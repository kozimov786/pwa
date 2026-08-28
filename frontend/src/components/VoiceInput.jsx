import { useRef, useState } from "react";
import { parseVoice } from "../api/client";

export default function VoiceInput({ onParsed }) {
  const [recording, setRecording] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  async function startRecording() {
    setError(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      chunksRef.current = [];
      recorder.ondataavailable = (e) => chunksRef.current.push(e.data);
      recorder.onstop = async () => {
        stream.getTracks().forEach((t) => t.stop());
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        setBusy(true);
        try {
          const parsed = await parseVoice(blob);
          onParsed(parsed);
        } catch (err) {
          setError(err.message);
        } finally {
          setBusy(false);
        }
      };
      recorder.start();
      mediaRecorderRef.current = recorder;
      setRecording(true);
    } catch {
      setError("Mikrofonga ruxsat berilmadi");
    }
  }

  function stopRecording() {
    mediaRecorderRef.current?.stop();
    setRecording(false);
  }

  return (
    <div className="flex items-center gap-3">
      <button
        onClick={recording ? stopRecording : startRecording}
        disabled={busy}
        className={`w-12 h-12 rounded-full flex items-center justify-center border transition-all
          ${recording ? "bg-neon-pink/20 border-neon-pink text-neon-pink animate-pulse" : "bg-base-700/60 border-white/10 hover:border-neon-cyan/60 hover:text-neon-cyan"}`}
        title="Ovozli buyruq"
      >
        {busy ? "…" : "🎙️"}
      </button>
      {recording && <span className="text-sm text-neon-pink">Yozilmoqda…</span>}
      {error && <span className="text-sm text-red-400">{error}</span>}
    </div>
  );
}
