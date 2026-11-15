import { interpolate, useCurrentFrame } from "remotion";
import { clamp, useSemantic } from "./theme";
import {
  Body,
  Card,
  Cursor,
  Glyph,
  Head,
  Kicker,
  Photo,
  Stage,
  Tag,
} from "./UI";
import type { SemanticShot } from "./types";
import { Lamp3D } from "./Objects3D";

export const Workday: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  const { p } = useSemantic();
  return (
    <Stage shot={shot}>
      <Card style={{ position: "absolute", left: 0, width: 970, height: 570 }}>
        <Kicker>MỘT NGÀY LÀM VIỆC · VÍ DỤ</Kicker>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 20,
            marginTop: 32,
          }}
        >
          <Glyph kind="mail" size={55} color={p.accent} />
          <Body style={{ fontSize: 42, fontWeight: 700 }}>
            Email giới thiệu Mẫu A
          </Body>
        </div>
        <Tag style={{ marginTop: 25 }}>Bản nháp · Chưa gửi</Tag>
        <div
          style={{
            borderTop: `1px solid ${p.line}`,
            marginTop: 29,
            paddingTop: 26,
            display: "flex",
            flexDirection: "column",
            gap: 23,
          }}
        >
          {[
            "Tra hồ sơ sản phẩm",
            "Soạn và kiểm tra email",
            "Trả lời khách rồi quyết định",
          ].map((t) => (
            <div
              key={t}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 17,
                font: "34px Arial",
              }}
            >
              <Glyph kind="document" size={31} color={p.accent} />
              {t}
            </div>
          ))}
        </div>
      </Card>
      {shot.asset ? (
        <div
          style={{
            position: "absolute",
            right: 0,
            width: 700,
            height: 620,
            borderRadius: 18,
            overflow: "hidden",
          }}
        >
          <Photo asset={shot.asset} />
        </div>
      ) : (
        <Lamp3D width={730} />
      )}
    </Stage>
  );
};

export const WorkRole: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  const localFrame = useCurrentFrame(),
    { p, actionFrame } = useSemantic();
  const f = shot.continuityGroup ? actionFrame : localFrame;
  return (
    <Stage shot={shot}>
      {shot.asset ? (
        <div
          style={{
            position: "absolute",
            right: 0,
            width: 560,
            top: 0,
            bottom: 0,
            borderRadius: 18,
            overflow: "hidden",
          }}
        >
          <Photo asset={shot.asset} />
        </div>
      ) : null}
      <Card style={{ width: shot.asset ? 1130 : 1600, minHeight: 545 }}>
        <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
          <Glyph kind="person" size={70} color={p.accent} />
          <div>
            <Kicker>MỘT CHỨC DANH</Kicker>
            <Body style={{ fontSize: 47, fontWeight: 700, marginTop: 12 }}>
              Nhân viên kinh doanh
            </Body>
          </div>
        </div>
        <div
          style={{
            marginTop: 38,
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: 19,
          }}
        >
          {[
            ["mail", "Viết email"],
            ["document", "Tra cứu sản phẩm"],
            ["search", "Kiểm tra thông tin"],
            ["chat", "Trao đổi với khách"],
            ["check", "Quyết định cam kết"],
          ].map(([icon, label], i) => (
            <div
              key={label}
              style={{
                padding: "22px 24px",
                border: `1px solid ${i === 0 ? p.good : p.line}`,
                borderRadius: 9,
                display: "flex",
                alignItems: "center",
                gap: 18,
                font: "31px Arial",
                background: i === 0 ? p.soft : undefined,
                opacity: interpolate(f, [i * 2, i * 2 + 5], [0.68, 1], clamp),
              }}
            >
              <Glyph
                kind={icon}
                size={36}
                color={i === 0 ? p.good : p.accent}
              />
              {label}
              {i === 0 ? (
                <span
                  style={{ marginLeft: "auto", fontSize: 23, color: p.good }}
                >
                  {shot.mode === "change" ? "AI hỗ trợ" : "nhanh hơn"}
                </span>
              ) : null}
            </div>
          ))}
        </div>
        <Body style={{ fontSize: 32, color: p.muted, marginTop: 30 }}>
          Một thao tác thay đổi. Những phần việc khác vẫn còn.
        </Body>
      </Card>
    </Stage>
  );
};

export const Context: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  const { p } = useSemantic();
  const need = shot.mode === "client_need";
  return (
    <Stage shot={shot}>
      <div style={{ display: "flex", gap: 28 }}>
        <Card style={{ flex: 1 }}>
          <Kicker>
            {need ? "NHU CẦU THẬT CỦA KHÁCH" : "PHẦN THÔNG TIN ĐANG THIẾU"}
          </Kicker>
          <div
            style={{
              display: "flex",
              gap: 24,
              alignItems: "center",
              marginTop: 43,
            }}
          >
            <Glyph kind={need ? "chat" : "mail"} size={70} color={p.accent} />
            <Body style={{ fontSize: 43, fontWeight: 700 }}>
              Dùng đèn ở nơi không có ổ cắm
            </Body>
          </div>
          <div
            style={{
              marginTop: 43,
              display: "flex",
              flexDirection: "column",
              gap: 25,
            }}
          >
            {["Khách cần dùng không dây", "Mẫu A cần dây nguồn USB-C"].map(
              (t) => (
                <Tag key={t} bad style={{ fontSize: 33 }}>
                  {t}
                </Tag>
              ),
            )}
          </div>
        </Card>
        <Card style={{ flex: 1 }}>
          <Kicker>NHỮNG GÌ BẢN NHÁP CHƯA BIẾT</Kicker>
          <div style={{ font: "700 65px Arial", color: p.bad, marginTop: 45 }}>
            {need ? "Chưa phù hợp nhu cầu" : "“Phù hợp mọi góc làm việc”"}
          </div>
          <Body style={{ fontSize: 35, color: p.muted, marginTop: 30 }}>
            Câu nghe trơn tru
            <br />
            chưa thay được việc hiểu hoàn cảnh.
          </Body>
          <Tag bad style={{ marginTop: 35 }}>
            Chưa trả lời đúng nhu cầu
          </Tag>
        </Card>
      </div>
    </Stage>
  );
};

export const Decision: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  const { p } = useSemantic();
  return (
    <Stage shot={shot}>
      <div style={{ display: "flex", gap: 28 }}>
        <Card style={{ width: 1060 }}>
          <Kicker>TRƯỚC KHI CAM KẾT VỚI KHÁCH</Kicker>
          {[
            ["document", "Nguồn gốc: USB-C có dây · Không pin"],
            ["chat", "Khách cần dùng nơi không có ổ cắm"],
            ["check", "Trả lời: Mẫu A chưa phù hợp nhu cầu đó"],
          ].map(([icon, text]) => (
            <div
              key={text}
              style={{
                display: "flex",
                gap: 25,
                alignItems: "center",
                font: "37px Arial",
                padding: "31px 0",
                borderBottom: `1px solid ${p.line}`,
              }}
            >
              <Glyph kind={icon} size={43} color={p.accent} />
              {text}
            </div>
          ))}
        </Card>
        <Card
          style={{
            flex: 1,
            textAlign: "center",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            gap: 30,
          }}
        >
          <Glyph kind="person" size={65} color={p.accent} />
          <Head style={{ fontSize: 51 }}>Bạn quyết định.</Head>
          {["Sửa trả lời", "Nói rõ chưa phù hợp", "Không gửi lời hứa sai"].map(
            (t, i) => (
              <Tag key={t} good={i === 1} style={{ fontSize: 28 }}>
                {i === 1 ? "✓ " : ""}
                {t}
              </Tag>
            ),
          )}
        </Card>
      </div>
    </Stage>
  );
};

export const Disclaimer: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  const { p } = useSemantic();
  return (
    <Stage shot={shot} headline={shot.headline ?? "Tình huống minh họa."}>
      <Card style={{ width: 1480, minHeight: 460, padding: 55 }}>
        <Kicker>PHẠM VI CỦA VÍ DỤ</Kicker>
        <Body
          style={{
            fontSize: 45,
            lineHeight: 1.5,
            marginTop: 38,
            maxWidth: 1280,
          }}
        >
          {shot.detail ??
            "Đèn, tính năng, giá và thời gian trong ví dụ là dữ liệu giả định để bàn về từng phần công việc."}
        </Body>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 22,
            marginTop: 38,
            color: p.muted,
          }}
        >
          <Glyph kind="document" size={42} />
          <span style={{ font: "31px Arial" }}>
            Không phải dự báo nghề nghiệp của từng người.
          </span>
        </div>
      </Card>
    </Stage>
  );
};

export const CommentCTA: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  const f = useCurrentFrame(),
    { p, direction } = useSemantic();
  const text =
    direction === "long"
      ? "Tôi muốn thử nháp email cho khách."
      : "Tôi muốn thử đối chiếu bảng số.";
  const question = shot.mode === "question";
  return (
    <Stage shot={shot}>
      <Card style={{ width: 1580, minHeight: 510 }}>
        <Kicker>MỘT VIỆC CỤ THỂ CỦA BẠN</Kicker>
        {question ? (
          <div style={{ display: "flex", gap: 20, marginTop: 43 }}>
            {[
              ["mail", "Nháp email"],
              ["table", "Đối chiếu bảng"],
              ["chat", "Trả lời khách"],
            ].map(([icon, text]) => (
              <div
                key={text}
                style={{
                  flex: 1,
                  border: `2px solid ${p.line}`,
                  borderRadius: 12,
                  padding: 24,
                  font: "34px Arial",
                  display: "flex",
                  gap: 20,
                  alignItems: "center",
                }}
              >
                <Glyph kind={icon} color={p.accent} size={42} />
                {text}
              </div>
            ))}
          </div>
        ) : (
          <div
            style={{
              display: "flex",
              gap: 23,
              alignItems: "center",
              marginTop: 32,
            }}
          >
            <Glyph kind="chat" size={63} color={p.accent} />
            <Body style={{ fontSize: 43 }}>
              Bạn giao phần nào? Tự kiểm tra phần nào?
            </Body>
          </div>
        )}
        <div
          style={{
            border: `2px solid ${p.accent}`,
            borderRadius: 12,
            padding: 30,
            marginTop: 38,
            minHeight: 115,
            font: "36px Arial",
            lineHeight: 1.4,
            color: p.ink,
          }}
        >
          {question
            ? "Chọn một nhiệm vụ bạn muốn bóc tách…"
            : text.slice(
                0,
                Math.max(
                  8,
                  Math.round(interpolate(f, [0, 35], [8, text.length], clamp)),
                ),
              )}
          <span style={{ color: p.accent }}>|</span>
        </div>
        <div
          style={{
            display: "inline-flex",
            gap: 17,
            alignItems: "center",
            marginTop: 31,
            padding: "16px 27px",
            background: p.accent,
            color: p.bg,
            font: "700 31px Arial",
            borderRadius: 9,
          }}
        >
          Để lại một ví dụ <Glyph kind="arrow" size={30} />
        </div>
        <Cursor x={500} y={450} />
      </Card>
    </Stage>
  );
};

export const Subscribe: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  const { p } = useSemantic();
  return (
    <Stage shot={shot} headline={shot.headline ?? "Cùng thử. Cùng kiểm tra."}>
      {shot.asset ? (
        <div
          style={{
            position: "absolute",
            right: 0,
            width: 540,
            top: 0,
            bottom: 0,
            borderRadius: 18,
            overflow: "hidden",
          }}
        >
          <Photo asset={shot.asset} />
        </div>
      ) : null}
      {!shot.asset ? (
        <Card
          style={{
            position: "absolute",
            right: 0,
            top: 45,
            width: 560,
            padding: 30,
          }}
        >
          <Kicker>THỬ NGHIỆM TIẾP THEO</Kicker>
          {[
            ["mail", "Email Mẫu A"],
            ["document", "Nguồn: có dây, không pin"],
            ["search", "Kiểm tra giá và nhu cầu"],
            ["check", "Bạn quyết định gửi"],
          ].map(([icon, t]) => (
            <div
              key={t}
              style={{
                display: "flex",
                gap: 18,
                alignItems: "center",
                font: "29px Arial",
                padding: "24px 0",
                borderBottom: `1px solid ${p.line}`,
              }}
            >
              <Glyph kind={icon} color={p.accent} size={35} />
              {t}
            </div>
          ))}
        </Card>
      ) : null}
      <div style={{ width: 1060, padding: "35px 15px" }}>
        <div
          style={{
            font: "700 95px Bahnschrift,Arial",
            letterSpacing: 6,
            color: p.ink,
          }}
        >
          TYRANNO
        </div>
        <Body
          style={{
            fontSize: 42,
            lineHeight: 1.45,
            marginTop: 27,
            maxWidth: 1100,
          }}
        >
          Bóc tách một nhiệm vụ.
          <br />
          Thử bằng ví dụ. Kiểm tra kết quả.
        </Body>
        <div
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 20,
            marginTop: 43,
            padding: "20px 35px",
            background: p.accent,
            color: p.bg,
            borderRadius: 10,
            font: "700 36px Arial",
          }}
        >
          Đăng ký TYRANNO <Glyph kind="arrow" size={38} />
        </div>
        <div style={{ display: "flex", gap: 18, marginTop: 35 }}>
          {["Tạo nháp", "Kiểm tra", "Quyết định"].map((t) => (
            <Tag key={t}>{t}</Tag>
          ))}
        </div>
      </div>
    </Stage>
  );
};
