import { AbsoluteFill, Sequence, staticFile, useCurrentFrame } from "remotion";
import { Audio } from "@remotion/media";
import { SemanticContext, exampleDefaults, palettes } from "./theme";
import type { SemanticShot, SemanticTimeline } from "./types";
import {
  CustomerReply,
  EmailScene,
  ProductFacts,
  SourceCheck,
  ToneEdit,
  WrongClaim,
} from "./EmailScenes";
import {
  Feedback,
  Goal,
  QualityCompare,
  QualityGate,
  ReviewWork,
  SendGate,
  TaskMap,
  TimeLog,
  Trial,
  NeedBridge,
} from "./ProcessScenes";
import {
  CommentCTA,
  Context,
  Decision,
  Disclaimer,
  Subscribe,
  WorkRole,
  Workday,
} from "./StoryScenes";
import { Workbench } from "./Workbench";

const Scene: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  if (shot.continuityGroup === "workday") return <Workbench shot={shot} />;
  switch (shot.scene) {
    case "email_prompt":
    case "email_draft":
      return <EmailScene shot={shot} />;
    case "wrong_claim":
      return <WrongClaim shot={shot} />;
    case "customer_reply":
      return <CustomerReply shot={shot} />;
    case "product_facts":
      return <ProductFacts shot={shot} />;
    case "source_check":
      return <SourceCheck shot={shot} />;
    case "tone_edit":
      return <ToneEdit shot={shot} />;
    case "goal":
      return <Goal shot={shot} />;
    case "feedback":
      return <Feedback shot={shot} />;
    case "task_map":
      return <TaskMap shot={shot} />;
    case "send_gate":
      return <SendGate shot={shot} />;
    case "review_work":
      return <ReviewWork shot={shot} />;
    case "time_log":
      return <TimeLog shot={shot} />;
    case "quality_compare":
      return <QualityCompare shot={shot} />;
    case "trial":
      return <Trial shot={shot} />;
    case "quality_gate":
      return shot.mode === "blocked" ? (
        <SendGate shot={shot} />
      ) : (
        <QualityGate shot={shot} />
      );
    case "intro":
      return <Workday shot={shot} />;
    case "work_role":
      return <WorkRole shot={shot} />;
    case "context":
      return shot.mode === "client_need" ? (
        <NeedBridge shot={shot} />
      ) : (
        <Context shot={shot} />
      );
    case "decision":
      return <Decision shot={shot} />;
    case "disclaimer":
      return <Disclaimer shot={shot} />;
    case "comment_cta":
      return <CommentCTA shot={shot} />;
    case "subscribe":
      return <Subscribe shot={shot} />;
    default:
      throw new Error(`Semantic scene was not implemented: ${shot.scene}`);
  }
};

/** A shot must show a visible state/action matching its exact spoken clause. */
export const SemanticFilm: React.FC<{ data: SemanticTimeline }> = ({
  data,
}) => {
  const f = useCurrentFrame(),
    seconds = f / data.fps;
  const caption = data.captions.find(
    (c, i) =>
      seconds >= c.start &&
      seconds <
        (i === data.captions.length - 1 ? data.frames / data.fps : c.end),
  );
  const active = data.shots.find((s) => f >= s.start && f < s.end);
  if (!active) throw new Error(`Semantic timeline has no shot at frame ${f}`);
  if (!active.visible?.length || !active.proof)
    throw new Error(`Shot ${active.phrase} lacks a visible action and proof`);
  const groupStart =
    active.continuityStart ??
    (active.continuityGroup
      ? data.shots.find((s) => s.continuityGroup === active.continuityGroup)
          ?.start
      : active.start) ??
    active.start;
  // The workday's lamp/fact panel is one persistent object. A later close-up
  // of typing hands must not replace its product photograph between verbs.
  const workdayAsset =
    data.shots.find(
      (s) => s.continuityGroup === "workday" && s.scene === "intro",
    )?.asset ??
    data.shots.find(
      (s) => s.continuityGroup === "workday" && s.scene === "product_facts",
    )?.asset;
  const renderedShot =
    active.continuityGroup === "workday"
      ? { ...active, asset: workdayAsset }
      : active;
  const mediaScene =
    [
      "email_prompt",
      "email_draft",
      "customer_reply",
      "product_facts",
      "feedback",
      "review_work",
      "trial",
      "work_role",
      "intro",
      "subscribe",
    ].includes(active.scene) ||
    (active.scene === "goal" && active.mode === "product");
  const mediaCredit =
    active.continuityGroup === "workday"
      ? workdayAsset?.credit
      : mediaScene
        ? active.asset?.credit
        : undefined;
  return (
    <SemanticContext.Provider
      value={{
        direction: data.direction,
        example: { ...exampleDefaults, ...data.example },
        actionFrame: f - groupStart,
      }}
    >
      <AbsoluteFill style={{ background: palettes[data.direction].bg }}>
        <Sequence
          from={active.start}
          durationInFrames={active.end - active.start}
          key={active.start}
        >
          <Scene shot={renderedShot} />
        </Sequence>
        {caption ? (
          <div
            style={{
              position: "absolute",
              bottom: 45,
              left: 140,
              right: 140,
              display: "flex",
              justifyContent: "center",
            }}
          >
            <div
              style={{
                font: "35px Arial,sans-serif",
                lineHeight: 1.3,
                color: "#fffef6",
                background: "rgba(4,13,18,.90)",
                padding: "12px 23px",
                borderRadius: 7,
                textAlign: "center",
                maxWidth: 1640,
              }}
            >
              {caption.text.normalize("NFC")}
            </div>
          </div>
        ) : null}
        {mediaCredit ? (
          <div
            style={{
              position: "absolute",
              left: 90,
              bottom: 133,
              font: "17px Arial",
              color: palettes[data.direction].muted,
            }}
          >
            {mediaCredit} · Ảnh minh họa thao tác
          </div>
        ) : null}
        <Audio src={staticFile(data.audio)} />
      </AbsoluteFill>
    </SemanticContext.Provider>
  );
};
