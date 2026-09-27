#!/usr/bin/env bash
# Render QC helpers built on ffmpeg/ffprobe. Read-only on the input video.
#
#   qc.sh probe    <video>                          codec, size, fps, duration, audio
#   qc.sh loudness <video> [target_lufs]            EBU R128 integrated LUFS (target ±1, default -14) + true peak
#   qc.sh sheet    <video> [out.png] [cols] [rows]  contact sheet of evenly spaced frames
#   qc.sh stills   <video> <out-dir> <t1> [t2 …]    one PNG per timestamp (seconds)
#   qc.sh loop     <video> [tolerance_db]           seam (last -> first) vs a normal frame step (default 3 dB)
set -euo pipefail

usage() { sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//'; exit 2; }
die() { echo "error: $*" >&2; exit 2; }

cmd="${1:-}"
case "$cmd" in probe|loudness|sheet|stills|loop) ;; *) usage ;; esac
shift
video="${1:-}"
[ -n "$video" ] && [ -f "$video" ] || die "video file required"

for bin in ffmpeg ffprobe; do
  command -v "$bin" >/dev/null 2>&1 || die "$bin not found (install ffmpeg)"
done

duration() {
  local d
  d="$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$video")"
  awk -v d="$d" 'BEGIN { exit !(d + 0 > 0) }' || die "cannot read a positive duration (got '$d')"
  printf '%s' "$d"
}

# PSNR between two images; prints a number or "inf".
psnr() {
  ffmpeg -hide_banner -nostats -i "$1" -i "$2" -lavfi psnr -f null - 2>&1 \
    | sed -n 's/.*average:\([0-9.inf]*\).*/\1/p' | tail -1
}

case "$cmd" in
  probe)
    ffprobe -v error -select_streams v:0 \
      -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt \
      -of default=nw=1 "$video"
    ffprobe -v error -select_streams a:0 \
      -show_entries stream=codec_name,sample_rate,channels \
      -of default=nw=1 "$video" | sed 's/^/audio_/'
    echo "duration=$(duration)"
    ;;

  loudness)
    target="${2:--14}"
    out="$(ffmpeg -hide_banner -nostats -i "$video" -map 0:a:0 -af ebur128=peak=true -f null - 2>&1)" \
      || die "no audio stream or ffmpeg failed"
    summary="$(printf '%s\n' "$out" | sed -n '/Summary:/,$p')"
    lufs="$(printf '%s\n' "$summary" | awk '/I:/ {print $2; exit}')"
    peak="$(printf '%s\n' "$summary" | awk '/Peak:/ {print $2; exit}')"
    [ -n "$lufs" ] && [ -n "$peak" ] || die "could not parse ebur128 summary"
    echo "integrated_lufs=${lufs}"
    echo "true_peak_dbtp=${peak}"
    awk -v l="$lufs" -v p="$peak" -v t="$target" 'BEGIN {
      ok = 1
      if (l < t - 1 || l > t + 1) { printf "warn: integrated loudness outside %s ±1 LUFS\n", t; ok = 0 }
      if (p > -1.0) { print "warn: true peak above -1 dBTP"; ok = 0 }
      if (ok) printf "ok: loudness within %s ±1 LUFS, true peak <= -1 dBTP\n", t
    }'
    ;;

  sheet)
    out="${2:-contact-sheet.png}"; cols="${3:-4}"; rows="${4:-4}"
    n=$((cols * rows))
    dur="$(duration)"
    rate="$(awk -v n="$n" -v d="$dur" 'BEGIN { printf "%.6f", n / d }')"
    # timecode labels need drawtext (libfreetype); fall back to an unlabeled sheet
    ffmpeg -hide_banner -loglevel error -y -i "$video" \
      -vf "fps=${rate},scale=480:-2,drawtext=text='%{pts\\:hms}':x=8:y=8:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6,tile=${cols}x${rows}:padding=4:margin=4" \
      -frames:v 1 "$out" 2>/dev/null \
    || ffmpeg -hide_banner -loglevel error -y -i "$video" \
      -vf "fps=${rate},scale=480:-2,tile=${cols}x${rows}:padding=4:margin=4" \
      -frames:v 1 "$out"
    echo "sheet=$out ($n frames over ${dur}s)"
    ;;

  stills)
    outdir="${2:-}"; [ -n "$outdir" ] || die "output dir required"
    shift 2
    [ "$#" -gt 0 ] || die "at least one timestamp required"
    mkdir -p "$outdir"
    for t in "$@"; do
      f="$outdir/still_$(printf '%s' "$t" | tr '.:' '__').png"
      rm -f "$f"
      ffmpeg -hide_banner -loglevel error -y -ss "$t" -i "$video" -frames:v 1 "$f"
      [ -s "$f" ] || die "no frame at ${t}s (past the end?)"
      echo "still=$f"
    done
    ;;

  loop)
    # A seamless loop's last frame is one step BEFORE the first frame, not equal to it,
    # so the seam (last -> first) should look like any normal step (frame 0 -> frame 1).
    tol="${2:-3}"
    tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
    ffmpeg -hide_banner -loglevel error -y -i "$video" -frames:v 2 "$tmp/f%d.png" || die "cannot decode $video"
    ffmpeg -hide_banner -loglevel error -y -sseof -0.5 -i "$video" -update 1 "$tmp/last.png"
    [ -s "$tmp/f1.png" ] && [ -s "$tmp/f2.png" ] && [ -s "$tmp/last.png" ] || die "could not extract frames"
    step="$(psnr "$tmp/f1.png" "$tmp/f2.png")"
    seam="$(psnr "$tmp/last.png" "$tmp/f1.png")"
    echo "step_psnr_db=${step}"
    echo "seam_psnr_db=${seam}"
    if awk -v s="$seam" -v p="$step" -v t="$tol" 'BEGIN {
      if (s == "inf") exit 0                  # identical frames at the seam
      if (p == "inf") exit !(s + 0 >= 40)     # static opening: seam must be near-identical
      exit !(s + 0 >= p - t)                  # seam no worse than a normal step
    }'; then
      echo "ok: loop seam looks like a normal frame step"
    else
      echo "fail: loop seam jumps (seam below step - ${tol} dB)"; exit 1
    fi
    ;;
esac
