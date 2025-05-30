'use client';

import { useEffect, useState } from 'react';
import { io } from 'socket.io-client';

export default function Page() {
  const [text, setText] = useState('');
  const [response, setResponse] = useState('');

  const [data, setData] = useState<any>(null); //テスト用

  useEffect(() => {
    const socket = io('http://localhost:5000');
    socket.on('update', (msg) => {
      setData(msg);
    });
    return () => {
      socket.disconnect();
    };
  }, []);

  async function sendText() {
    try {
      const res = await fetch('http://localhost:5000/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ text }),
      });
      const data = await res.json();
      setResponse(JSON.stringify(data, null, 2));
    } catch (error: any) {
      setResponse('送信エラー: ' + error.message);
    }
  }


  return (
    <main>
      <h1>TalkFlow</h1>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={5}
        cols={40}
        placeholder="テキストを入力してください"
      />
      <br />
      <button onClick={sendText}>送信</button>
      <h2>Test</h2>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </main>
  );
}
