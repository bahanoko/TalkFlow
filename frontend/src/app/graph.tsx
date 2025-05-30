'use client';

import React, { useRef, useEffect, useState } from 'react';
import dynamic from 'next/dynamic';

const ForceGraph2D = dynamic(() => import('react-force-graph-2d'), { ssr: false });

type Node = { id: string };
type Link = { source: string; target: string; weight?: number };

type GraphData = {
   nodes: Node[];
   links: Link[];
};

type GraphViewProps = {
   data: GraphData;
   latestNodeId?: string | null;
};

export default function GraphView({ data, latestNodeId }: GraphViewProps) {
   const hoverNode = useRef<string | null>(null);
   const containerRef = useRef<HTMLDivElement>(null);
   const [size, setSize] = useState({ width: 700, height: 600 });
   const fgRef = useRef<any>(null);

   useEffect(() => {
      function handleResize() {
         if (containerRef.current) {
            setSize({
               width: containerRef.current.offsetWidth,
               height: containerRef.current.offsetHeight,
            });
         }
      }
      handleResize();
      window.addEventListener('resize', handleResize);
      return () => window.removeEventListener('resize', handleResize);
   }, []);


   useEffect(() => {
      if (fgRef.current) {
         fgRef.current.d3Force('link')?.distance(180); // Node間距離
      }
   }, [data]);

   return (
      <div
         ref={containerRef}
         className="card"
         style={{
            width: "100%",
            maxWidth: 700,
            height: 600,
            background: "#232329",
            borderRadius: 18,
            boxShadow: "0 4px 32px #000a",
            position: "relative",
            overflow: "hidden",
         }}
      >
         <ForceGraph2D
            ref={fgRef}
            width={size.width}
            height={size.height}
            graphData={data}
            backgroundColor="#232329"
            nodeRelSize={8}
            nodeCanvasObject={(node, ctx, globalScale) => {
               const isHover = node.id === hoverNode.current;
               const isLatest = latestNodeId && node.id === latestNodeId;
               ctx.beginPath();
               ctx.arc(node.x!, node.y!, isHover ? 12 : 8, 0, 2 * Math.PI, false);
               ctx.fillStyle = isLatest ? "#ef4444" : (isHover ? "#06b6d4" : "#fff");
               ctx.shadowColor = isHover ? "#06b6d4" : "#000";
               ctx.shadowBlur = isHover ? 16 : 0;
               ctx.fill();
               ctx.shadowBlur = 0;
               ctx.font = `${16 / globalScale}px var(--font-geist-sans), sans-serif`;
               ctx.textAlign = 'center';
               ctx.textBaseline = 'top';
               ctx.fillStyle = isLatest ? "#ef4444" : (isHover ? "#06b6d4" : "#fff");
               ctx.fillText(String(node.id), node.x!, node.y! + 12);
            }}
            nodePointerAreaPaint={(node, color, ctx) => {
               ctx.beginPath();
               ctx.arc(node.x!, node.y!, 14, 0, 2 * Math.PI, false);
               ctx.fillStyle = color;
               ctx.fill();
            }}
            linkColor={() => "#6366f1"}
            linkDirectionalParticles={2}
            linkDirectionalArrowLength={4}
            linkWidth={(link: any) => (link.weight ? link.weight * 2 : 1.5)}
            onNodeHover={node => {
               hoverNode.current = node ? String(node.id) : null;
            }}
         />
      </div>
   );
}
