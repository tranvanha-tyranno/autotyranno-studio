import type { CSSProperties, ReactNode } from "react";
import {
  AbsoluteFill,
  CanvasImage,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";
import { clamp, useSemantic } from "./theme";
import type { SemanticAsset, SemanticShot } from "./types";

export const Glyph: React.FC<{
  kind: string;
  size?: number;
  color?: string;
}> = ({ kind, size = 42, color = "currentColor" }) => {
  const paths: Record<string, ReactNode> = {
    mail: (
      <>
        <rect x="3" y="6" width="26" height="20" rx="3" />
        <path d="m4 8 12 10L28 8" />
      </>
    ),
    document: (
      <>
        <path d="M8 3h11l6 6v20H8zM19 3v7h6M12 16h9M12 21h9" />
      </>
    ),
    check: <path d="m5 17 7 7L28 7" />,
    cross: <path d="m7 7 18 18M25 7 7 25" />,
    arrow: <path d="M3 16h25m-8-8 8 8-8 8" />,
    person: (
      <>
        <circle cx="16" cy="9" r="5" />
        <path d="M5 29v-5c0-9 22-9 22 0v5" />
      </>
    ),
    chat: <path d="M4 4h24v19H14l-8 6v-6H4zM10 11h12M10 16h8" />,
    clock: (
      <>
        <circle cx="16" cy="16" r="13" />
        <path d="M16 7v10l6 4" />
      </>
    ),
    search: (
      <>
        <circle cx="13" cy="13" r="9" />
        <path d="m20 20 9 9" />
      </>
    ),
    lock: (
      <>
        <rect x="6" y="14" width="20" height="16" rx="3" />
        <path d="M10 14V9a6 6 0 0 1 12 0v5M16 21v4" />
      </>
    ),
    table: (
      <>
        <rect x="3" y="5" width="26" height="23" rx="2" />
        <path d="M3 12h26M3 20h26M13 5v23" />
      </>
    ),
    lamp: (
      <>
        <path d="M4 29h24M16 29V15l8-8M17 6l10-3 3 10-13-7z" />
      </>
    ),
  };
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      fill="none"
      stroke={color}
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      style={{ flexShrink: 0 }}
    >
      {paths[kind] ?? paths.document}
    </svg>
  );
};

export const Tag: React.FC<{
  children: ReactNode;
  good?: boolean;
  bad?: boolean;
  style?: CSSProperties;
}> = ({ children, good, bad, style }) => {
  const { p } = useSemantic();
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 12,
        padding: "10px 17px",
        border: `1px solid ${bad ? p.bad : good ? p.good : p.line}`,
        color: bad ? p.bad : good ? p.good : p.muted,
        font: "24px Arial,sans-serif",
        lineHeight: 1.2,
        borderRadius: 7,
        ...style,
      }}
    >
      {children}
    </span>
  );
};
export const Card: React.FC<{ children: ReactNode; style?: CSSProperties }> = ({
  children,
  style,
}) => {
  const { p } = useSemantic();
  return (
    <div
      style={{
        background: p.surface,
        border: `1px solid ${p.line}`,
        borderRadius: 18,
        boxShadow: p.shadow,
        padding: 36,
        color: p.ink,
        ...style,
      }}
    >
      {children}
    </div>
  );
};
export const Kicker: React.FC<{
  children: ReactNode;
  style?: CSSProperties;
}> = ({ children, style }) => {
  const { p } = useSemantic();
  return (
    <div
      style={{
        font: "700 23px Arial,sans-serif",
        letterSpacing: 2.2,
        color: p.muted,
        lineHeight: 1.3,
        ...style,
      }}
    >
      {children}
    </div>
  );
};
export const Body: React.FC<{ children: ReactNode; style?: CSSProperties }> = ({
  children,
  style,
}) => {
  const { p } = useSemantic();
  return (
    <div
      style={{
        font: "38px Arial,sans-serif",
        lineHeight: 1.4,
        color: p.ink,
        ...style,
      }}
    >
      {children}
    </div>
  );
};
export const Head: React.FC<{ children?: string; style?: CSSProperties }> = ({
  children,
  style,
}) => {
  const { p } = useSemantic();
  return children ? (
    <div
      style={{
        fontFamily: p.heading,
        fontSize: children.length > 60 ? 62 : 76,
        lineHeight: 1.08,
        letterSpacing: -1.3,
        fontWeight: 600,
        overflowWrap: "break-word",
        ...style,
      }}
    >
      {children.normalize("NFC")}
    </div>
  ) : null;
};
export const Photo: React.FC<{
  asset: SemanticAsset;
  style?: CSSProperties;
}> = ({ asset, style }) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ overflow: "hidden", ...style }}>
      <CanvasImage
        src={staticFile(asset.file)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          objectPosition: `${asset.focus?.[0] ?? 50}% ${asset.focus?.[1] ?? 50}%`,
          scale: 1.01 + Math.min(f, 150) * 0.00015,
        }}
      />
    </AbsoluteFill>
  );
};
export const Cursor: React.FC<{ x: number; y: number; delay?: number }> = ({
  x,
  y,
  delay = 0,
}) => {
  const f = useCurrentFrame(),
    { p } = useSemantic();
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        translate: `${interpolate(f, [delay, delay + 16], [60, 0], clamp)}px ${interpolate(f, [delay, delay + 16], [35, 0], clamp)}px`,
        opacity: interpolate(f, [delay, delay + 5], [0, 1], clamp),
        zIndex: 5,
      }}
    >
      <svg width="45" height="56" viewBox="0 0 35 45">
        <path
          d="M3 2v35l10-9 7 14 7-4-7-13h12z"
          fill={p.ink}
          stroke={p.surface}
          strokeWidth="2"
        />
      </svg>
    </div>
  );
};
export const Highlight: React.FC<{
  children: ReactNode;
  bad?: boolean;
  style?: CSSProperties;
}> = ({ children, bad, style }) => {
  const f = useCurrentFrame(),
    { p } = useSemantic();
  return (
    <span
      style={{
        position: "relative",
        display: "inline-block",
        padding: "5px 12px",
        color: bad ? p.bad : p.ink,
        ...style,
      }}
    >
      <span
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          bottom: 0,
          width: `${interpolate(f, [0, 14], [35, 100], clamp)}%`,
          background: bad ? p.bad + "22" : p.soft,
          borderBottom: `3px solid ${bad ? p.bad : p.accent}`,
        }}
      />
      <span style={{ position: "relative" }}>{children}</span>
    </span>
  );
};
export const Stage: React.FC<{
  shot: SemanticShot;
  children: ReactNode;
  headline?: string;
  style?: CSSProperties;
}> = ({ shot, children, headline, style }) => {
  const { p, direction } = useSemantic();
  return (
    <AbsoluteFill
      style={{
        background:
          direction === "long"
            ? "radial-gradient(ellipse at 60% 40%,#fbf7ee,#e9e3d8)"
            : "radial-gradient(ellipse at 60% 45%,#163544,#081923 76%)",
        color: p.ink,
        fontFamily: "Arial,sans-serif",
        overflow: "hidden",
        ...style,
      }}
    >
      <div
        style={{
          position: "absolute",
          left: 90,
          top: 60,
          right: 90,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          gap: 30,
        }}
      >
        <Kicker>
          {shot.phase === "hook"
            ? "MỘT VÍ DỤ ĐỂ NHÌN RÕ"
            : shot.phase === "cta"
              ? "ĐẾN LƯỢT BẠN"
              : shot.phase === "disclaimer"
                ? "LƯU Ý"
                : "ĐÈN BÀN MẪU A · MỘT NGÀY LÀM VIỆC"}
        </Kicker>
        <div
          style={{
            font: "20px Arial,sans-serif",
            color: p.muted,
            letterSpacing: 1.2,
          }}
        >
          VÍ DỤ MINH HỌA · DỮ LIỆU GIẢ ĐỊNH
        </div>
      </div>
      {(headline ?? shot.headline) ? (
        <div style={{ position: "absolute", left: 90, top: 118, right: 90 }}>
          <Head>{headline ?? shot.headline}</Head>
        </div>
      ) : null}
      <AbsoluteFill
        style={{
          top: (headline ?? shot.headline) ? 250 : 140,
          bottom: 170,
          left: 90,
          right: 90,
          height: "auto",
          width: "auto",
        }}
      >
        {children}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
