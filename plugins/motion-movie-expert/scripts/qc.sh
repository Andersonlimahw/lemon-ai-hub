#!/usr/bin/env bash
# Render QC helpers built on ffmpeg/ffprobe. Read-only on the input video.
#
#   qc.sh probe    <video>                      codec, size, fps, duration, audio
#   qc.sh loudness <video>                      EBU R128 integrated LUFS + true peak
#   qc.sh sheet    <video> [out.png] [cols] [rows]  contact sheet of evenly spaced frames
#   qc.sh stills   <video> <out-dir> <t1> [t2 …]    one PNG per timestamp (seconds)
#   qc.sh loop     <video> [min_psnr_db]        first vs last frame similarity (default 40 dB)
set -euo pipefail

die() { echo "error: $*" >&2; exit 2; }
need() { command -v "$1" >/dev/null 2>&1 || die "$1 not found (install ffmpeg)"; }
need ffmpeg
need ffprobe

cmd="${1:-}"; shift || true
[ -n "$cmd" ] || { sed -n '2,9p' "$0"; exit 2; }
video="${1:-}"
[ -n "$video" ] && [ -f "$video" ] || die "video file required"

duration() {
  ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$video"
}

case "$cmd" in
  probe)
    ffprobe -v error -select_streams v:0 \
      -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt \
      -of default=nw=1 "$video"
    ffprobe -v error -select_streams a:0 \
      -show_entries stream=codec_name,sample_rate,channels \
      -of default=nw=1 "$video" | sed 's/^/audio_/' || true
    echo "duration=$(duration)"
    ;;

  loudness)
    out="$(ffmpeg -hide_banner -nostats -i "$video" -map 0:a:0 -af ebur128=peak=true -f null - 2>&1)" \
      || die "no audio stream or ffmpeg failed"
    summary="$(printf '%s\n' "$out" | sed -n '/Summary:/,$p')"
    lufs="$(printf '%s\n' "$summary" | awk '/I:/ {print $2; exit}')"
    peak="$(printf '%s\n' "$summary" | awk '/Peak:/ {print $2; exit}')"
    echo "integrated_lufs=${lufs}"
    echo "true_peak_dbtp=${peak}"
    awk -v l="$lufs" -v p="$peak" 'BEGIN {
      ok = 1
      if (l < -16.5 || l > -13.5) { print "warn: integrated loudness outside -14..-16 LUFS (web/social target)"; ok = 0 }
      if (p > -1.0) { print "warn: true peak above -1 dBTP"; ok = 0 }
      if (ok) print "ok: loudness within web/social targets"
    }'
    ;;

  sheet)
    out="${2:-contact-sheet.png}"; cols="${3:-4}"; rows="${4:-4}"
    n=$((cols * rows))
    dur="$(duration)"
    rate="$(awk -v n="$n" -v d="$dur" 'BEGIN { printf "%.6f", n / d }')"
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
    shift 2 || true
    [ "$#" -gt 0 ] || die "at least one timestamp required"
    mkdir -p "$outdir"
    for t in "$@"; do
      f="$outdir/still_$(printf '%s' "$t" | tr '.:' '__').png"
      ffmpeg -hide_banner -loglevel error -y -ss "$t" -i "$video" -frames:v 1 "$f"
      echo "still=$f"
    done
    ;;

  loop)
    min="${2:-40}"
    tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
    ffmpeg -hide_banner -loglevel error -y -i "$video" -frames:v 1 "$tmp/first.png"
    ffmpeg -hide_banner -loglevel error -y -sseof -0.5 -i "$video" -update 1 "$tmp/last.png"
    psnr="$(ffmpeg -hide_banner -nostats -i "$tmp/first.png" -i "$tmp/last.png" \
      -lavfi psnr -f null - 2>&1 | sed -n 's/.*average:\([0-9.inf]*\).*/\1/p' | tail -1)"
    echo "loop_psnr_db=${psnr}"
    if [ "$psnr" = "inf" ] || awk -v p="$psnr" -v m="$min" 'BEGIN { exit !(p >= m) }'; then
      echo "ok: first and last frames match (>= ${min} dB)"
    else
      echo "fail: loop seam visible (< ${min} dB)"; exit 1
    fi
    ;;

  *) die "unknown command: $cmd (probe|loudness|sheet|stills|loop)" ;;
esac
