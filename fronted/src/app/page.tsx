"use client";

import { useEffect, useRef, useState } from "react";
import { io } from "socket.io-client";
import GraphView from "./graph";
import isEqual from "lodash.isequal";

const EMPTY_GRAPH = { nodes: [], links: [] };

export default function Page() {
  const [text, setText] = useState("");
  const [response, setResponse] = useState("");
  const [data, setData] = useState<any>(null);

  const prevDataRef = useRef<any>(null);

  useEffect(() => {
    const socket = io("http://localhost:5000");
    socket.on("update", (msg) => {
      // 前回と異なる場合のみ更新
      if (!isEqual(prevDataRef.current, msg)) {
        setData(msg);
        prevDataRef.current = msg;
      }
    });
    return () => {
      socket.disconnect();
    };
  }, []);

  async function sendText() {
    try {
      const res = await fetch("http://localhost:5000/send", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ text }),
      });
      const data = await res.json();
      setResponse(JSON.stringify(data, null, 2));
    } catch (error: any) {
      setResponse("送信エラー: " + error.message);
    }
  }

  async function handleReset() {
    await fetch("http://localhost:5000/reset", { method: "POST" });
    setData(EMPTY_GRAPH);
  }

  return (
    <main>
      <h1>TalkFlow</h1>
      <div className="card">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={5}
          cols={40}
          placeholder="テキストを入力してください"
        />
        <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem" }}>
          <button onClick={sendText}>送信</button>
          <button onClick={handleReset} style={{ background: "#6366f1" }}>
            リセット
          </button>
        </div>
      </div>
      <GraphView data={data ?? EMPTY_GRAPH} />
    </main>
  );
}
