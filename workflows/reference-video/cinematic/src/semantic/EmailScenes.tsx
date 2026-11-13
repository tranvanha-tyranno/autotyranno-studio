import { interpolate, useCurrentFrame } from "remotion";
import { clamp, currency, useSemantic } from "./theme";
import {
  Body,
  Card,
  Cursor,
  Glyph,
  Highlight,
  Kicker,
  Photo,
  Stage,
  Tag,
} from "./UI";
import { Lamp3D } from "./Objects3D";
import type { SemanticShot } from "./types";

export const EmailScene: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  const localFrame = useCurrentFrame(),
    { p, example: e, actionFrame } = useSemantic();
  const f = shot.continuityGroup ? actionFrame : localFrame;
  const prompt =
    shot.mode === "revised"
      ? "Viết email giới thiệu Mẫu A. Chỉ dùng thông tin gốc; thiếu gì hãy hỏi lại."
      : "Viết email chào hàng cho đèn bàn Mẫu A.";
  const showingPrompt = shot.scene === "email_prompt";
  const draftReady = shot.mode !== "typing";
  const structure = shot.mode === "structure";
  return (
    <Stage shot={shot}>
      {shot.asset ? (
        <div
          style={{
            position: "absolute",
            right: 0,
            width: 525,
            top: 0,
            bottom: 0,
            borderRadius: 18,
            overflow: "hidden",
          }}
        >
          <Photo asset={shot.asset} />
        </div>
      ) : null}
      <Card
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          width: shot.asset ? 1130 : 1490,
          height: 620,
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 18,
            borderBottom: `1px solid ${p.line}`,
            paddingBottom: 23,
          }}
        >
          <Glyph kind="mail" color={p.accent} />
          <Kicker>
            {showingPrompt
              ? "GIAO VIỆC CHO AI"
              : "EMAIL CHÀO HÀNG · BẢN NHÁP BAN ĐẦU"}
          </Kicker>
          <Tag style={{ marginLeft: "auto" }}>Chưa gửi</Tag>
        </div>
        {showingPrompt && structure ? (
          <>
            <Kicker style={{ marginTop: 35 }}>KHUNG CẤU TRÚC ĐƯỢC GỢI Ý</Kicker>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "1fr 1fr",
                gap: 18,
                marginTop: 25,
              }}
            >
              {[
                "Chào khách",
                "Giới thiệu sản phẩm",
                "Đối chiếu nhu cầu",
                "Hỏi lại điều còn thiếu",
              ].map((t, i) => (
                <Tag key={t} style={{ fontSize: 31, padding: 20 }}>
                  {i + 1}. {t}
                </Tag>
              ))}
            </div>
            <Tag bad style={{ marginTop: 35 }}>
              Chưa điền cam kết tính năng
            </Tag>
          </>
        ) : showingPrompt ? (
          <>
            <Body
              style={{
                fontSize: 43,
                maxWidth: shot.asset ? 990 : 1320,
                marginTop: 46,
                minHeight: 150,
              }}
            >
              {prompt.slice(
                0,
                Math.max(
                  14,
                  Math.round(
                    interpolate(
                      f,
                      [0, Math.min(24, shot.end - shot.start - 1)],
                      [14, prompt.length],
                      clamp,
                    ),
                  ),
                ),
              )}
              <span
                style={{
                  color: p.accent,
                  opacity: Math.floor(f / 9) % 2 ? 0 : 1,
                }}
              >
                |
              </span>
            </Body>
            <div
              style={{
                display: "flex",
                gap: 16,
                marginTop: 32,
                flexWrap: "wrap",
              }}
            >
              {[
                "Sản phẩm: Mẫu A",
                "Người đọc: khách hàng",
                "Không hứa ngoài nguồn",
              ]
                .slice(0, shot.mode === "revised" ? 3 : 1)
                .map((t) => (
                  <Tag key={t}>{t}</Tag>
                ))}
            </div>
            <div
              style={{
                position: "absolute",
                left: 38,
                bottom: 40,
                display: "flex",
                alignItems: "center",
                gap: 20,
                background: p.accent,
                color: p.bg,
                padding: "18px 28px",
                borderRadius: 10,
                font: "700 33px Arial",
              }}
            >
              Tạo bản nháp <Glyph kind="arrow" size={34} />
            </div>
            <Cursor x={332} y={516} />
          </>
        ) : (
          <>
            <div style={{ font: "26px Arial", color: p.muted, marginTop: 28 }}>
              Đến: khach@vidu.invalid
            </div>
            <Body style={{ fontWeight: 700, fontSize: 40, marginTop: 17 }}>
              Giới thiệu {e.productName}
            </Body>
            <Body
              style={{
                fontSize: 35,
                marginTop: 22,
                lineHeight: 1.45,
                maxWidth: 1290,
              }}
            >
              Chào anh/chị,
              <br />
              Mua ngay!
              <br />
              <span
                style={{
                  opacity: draftReady
                    ? 1
                    : interpolate(f, [12, 20], [0, 1], clamp),
                }}
              >
                {e.unsupportedFeature}. Giá {currency(e.draftPriceVND)}.
              </span>
            </Body>
            <div
              style={{
                position: "absolute",
                bottom: 38,
                left: 38,
                right: 38,
                display: "flex",
                alignItems: "center",
                gap: 18,
              }}
            >
              <Tag>AI tạo nháp</Tag>
              <Tag bad>Chưa kiểm tra</Tag>
              <div
                style={{
                  marginLeft: "auto",
                  font: "28px Arial",
                  color: p.muted,
                }}
              >
                Gửi <Glyph kind="lock" size={30} />
              </div>
            </div>
          </>
        )}
      </Card>
    </Stage>
  );
};

export const WrongClaim: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  const { p, example: e } = useSemantic();
  return (
    <Stage shot={shot}>
      <Card
        style={{
          position: "absolute",
          left: 0,
          top: 8,
          width: 900,
          height: 570,
        }}
      >
        <Kicker>TRONG EMAIL NHÁP</Kicker>
        <div style={{ font: "700 59px Arial", margin: "48px 0 30px" }}>
          <Highlight bad>{e.unsupportedFeature}</Highlight>
        </div>
        <Tag bad>
          <Glyph kind="cross" size={30} /> Không có trong thông tin gốc
        </Tag>
        <Body style={{ fontSize: 34, marginTop: 37, color: p.muted }}>
          Một câu nghe hợp lý.
          <br />
          Một tính năng chưa được xác nhận.
        </Body>
      </Card>
      <div style={{ position: "absolute", right: 0, width: 800, height: 620 }}>
        <Lamp3D width={800} />
        <div style={{ position: "absolute", bottom: 5, left: 70, right: 35 }}>
          <Tag good style={{ fontSize: 29, background: p.surface }}>
            Nguồn USB-C có dây · Không pin
          </Tag>
        </div>
      </div>
    </Stage>
  );
};

export const CustomerReply: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  const { p, example: e } = useSemantic();
  const upset = shot.mode === "upset";
  return (
    <Stage shot={shot}>
      {shot.asset ? (
        <div
          style={{
            position: "absolute",
            right: 0,
            width: 530,
            top: 0,
            bottom: 0,
            borderRadius: 18,
            overflow: "hidden",
          }}
        >
          <Photo asset={shot.asset} />
        </div>
      ) : null}
      {upset ? (
        <>
          <Lamp3D width={670} connected={false} />
          <Tag
            bad
            style={{
              position: "absolute",
              right: 40,
              bottom: 20,
              fontSize: 29,
            }}
          >
            Rút cáp · Đèn tắt · Không pin
          </Tag>
        </>
      ) : null}
      <div style={{ width: upset ? 1010 : shot.asset ? 1120 : 1500 }}>
        <Card style={{ padding: 35 }}>
          <Kicker>PHẢN HỒI GIẢ ĐỊNH NẾU GỬI EMAIL</Kicker>
          <div
            style={{
              display: "flex",
              gap: 26,
              alignItems: "center",
              marginTop: 30,
            }}
          >
            <Glyph kind="chat" size={70} color={p.accent} />
            <Body style={{ fontSize: 43 }}>
              {upset
                ? "“Email nói không dây, sao rút cáp đèn không sáng?”"
                : "“Đèn có pin để mang ra ngoài đúng không?”"}
            </Body>
          </div>
        </Card>
        <div
          style={{
            display: "flex",
            gap: 25,
            alignItems: "center",
            margin: "38px 45px",
          }}
        >
          <Glyph kind="arrow" size={50} />
          <Tag bad style={{ fontSize: 31 }}>
            Người gửi email phải xác nhận lại
          </Tag>
        </div>
        <Card style={{ width: "91%", marginLeft: "9%" }}>
          <Kicker>HỘP TRẢ LỜI CỦA BẠN</Kicker>
          <Body style={{ fontSize: 38, marginTop: 24 }}>
            Kiểm tra lại thông tin của {e.productName}…
          </Body>
          <div style={{ font: "26px Arial", color: p.muted, marginTop: 28 }}>
            Chưa gửi · Đang xác minh
          </div>
        </Card>
      </div>
    </Stage>
  );
};

export const ProductFacts: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  const { p, example: e } = useSemantic();
  return (
    <Stage shot={shot}>
      <Card
        style={{
          position: "absolute",
          left: 0,
          top: 10,
          width: 875,
          height: 570,
        }}
      >
        <Kicker>HỒ SƠ SẢN PHẨM GIẢ ĐỊNH</Kicker>
        <Body style={{ fontSize: 46, fontWeight: 700, marginTop: 30 }}>
          {e.productName}
        </Body>
        <div
          style={{
            borderTop: `1px solid ${p.line}`,
            marginTop: 30,
            paddingTop: 22,
          }}
        >
          {[
            ["Nguồn", "USB-C có dây"],
            ["Pin", "Không có"],
            ["Giá", currency(e.sourcePriceVND)],
          ].map(([a, b]) => (
            <div
              key={a}
              style={{
                display: "flex",
                justifyContent: "space-between",
                padding: "16px 0",
                font: "35px Arial",
                borderBottom: `1px solid ${p.line}`,
              }}
            >
              <span style={{ color: p.muted }}>{a}</span>
              <strong>{b}</strong>
            </div>
          ))}
        </div>
        <Tag good style={{ marginTop: 28 }}>
          <Glyph kind="check" size={28} /> Chỉ cam kết điều có trong nguồn
        </Tag>
      </Card>
      {shot.asset ? (
        <div
          style={{
            position: "absolute",
            right: 0,
            top: 0,
            width: 790,
            height: 620,
            borderRadius: 18,
            overflow: "hidden",
          }}
        >
          <Photo asset={shot.asset} />
          <div
            style={{
              position: "absolute",
              left: 22,
              bottom: 22,
              padding: "10px 15px",
              background: p.surface,
              color: p.muted,
              font: "20px Arial",
            }}
          >
            Ảnh đèn minh họa · Thông số thuộc ví dụ giả định
          </div>
        </div>
      ) : (
        <Lamp3D />
      )}
    </Stage>
  );
};

export const SourceCheck: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  const f = useCurrentFrame(),
    { p, example: e } = useSemantic();
  const original = shot.mode === "original";
  const corrected = shot.mode === "reconcile";
  return (
    <Stage shot={shot}>
      {shot.asset ? (
        <div
          style={{
            position: "absolute",
            right: 0,
            width: 470,
            top: 0,
            bottom: 0,
            borderRadius: 18,
            overflow: "hidden",
          }}
        >
          <Photo asset={shot.asset} />
        </div>
      ) : null}
      <div
        style={{ display: "flex", gap: 24, width: shot.asset ? 1220 : 1720 }}
      >
        <Card style={{ flex: 1, padding: 30 }}>
          <Kicker>BẢNG THÔNG TIN GỐC</Kicker>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 18,
              margin: "26px 0",
            }}
          >
            <Glyph kind="table" size={45} color={p.accent} />
            <Body style={{ fontSize: 34, fontWeight: 700 }}>MẪU A</Body>
          </div>
          {[
            ["Nguồn", "USB-C có dây"],
            ["Pin", "Không có"],
            ["Giá", currency(e.sourcePriceVND)],
          ].map(([a, b]) => (
            <div
              key={a}
              style={{
                display: "flex",
                justifyContent: "space-between",
                gap: 14,
                font: "31px Arial",
                padding: "22px 5px",
                borderTop: `1px solid ${p.line}`,
                background: a === "Giá" ? p.soft : undefined,
              }}
            >
              <span style={{ color: p.muted }}>{a}</span>
              <strong>{b}</strong>
            </div>
          ))}
          <div style={{ font: "23px Arial", color: p.muted, marginTop: 22 }}>
            Dữ liệu giả định cho ví dụ
          </div>
        </Card>
        <Card style={{ flex: 1, padding: 30 }}>
          <Kicker>
            {corrected
              ? "BẢN NHÁP ĐÃ SỬA"
              : original
                ? "BẢNG TÓM TẮT CẦN ĐỐI CHIẾU"
                : "BẢN NHÁP BAN ĐẦU"}
          </Kicker>
          <div style={{ marginTop: 32 }}>
            <Body style={{ fontSize: 31, color: p.bad }}>
              {e.unsupportedFeature}
            </Body>
            <div
              style={{
                font: "700 52px Arial",
                marginTop: 24,
                color: corrected ? p.good : p.bad,
              }}
            >
              {currency(corrected ? e.sourcePriceVND : e.draftPriceVND)}
            </div>
            <div
              style={{
                height: 4,
                width: interpolate(f, [0, 15], [0, 100], clamp) + "%",
                background: corrected ? p.good : p.bad,
                margin: "25px 0 29px",
              }}
            />
            <Tag good={corrected} bad={!corrected} style={{ fontSize: 27 }}>
              <Glyph kind={corrected ? "check" : "cross"} size={30} />
              {corrected
                ? "Giá khớp · Còn lỗi tính năng"
                : "Thông tin chưa khớp"}
            </Tag>
          </div>
          <Body style={{ fontSize: 29, marginTop: 29, color: p.muted }}>
            Nối từng dòng về nguồn.
            <br />
            Không tin chỉ vì trình bày đẹp.
          </Body>
        </Card>
      </div>
    </Stage>
  );
};

export const ToneEdit: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  const { p } = useSemantic();
  return (
    <Stage shot={shot}>
      <div style={{ display: "flex", gap: 26 }}>
        <Card style={{ flex: 1, minHeight: 480 }}>
          <Kicker>BẢN NHÁP BAN ĐẦU</Kicker>
          <Body style={{ fontSize: 44, marginTop: 50, lineHeight: 1.5 }}>
            “Mua ngay!”
          </Body>
          <div style={{ marginTop: 45 }}>
            <Tag bad>Giọng thúc ép</Tag>
          </div>
        </Card>
        <Card style={{ flex: 1, minHeight: 480, borderColor: p.good }}>
          <Kicker>SAU KHI SỬA GIỌNG ĐIỆU</Kicker>
          <Body style={{ fontSize: 44, marginTop: 50, lineHeight: 1.5 }}>
            “Mời bạn tham khảo.”
          </Body>
          <div style={{ marginTop: 45 }}>
            <Tag good>
              <Glyph kind="check" size={28} /> Phù hợp người đọc
            </Tag>
          </div>
        </Card>
      </div>
    </Stage>
  );
};
