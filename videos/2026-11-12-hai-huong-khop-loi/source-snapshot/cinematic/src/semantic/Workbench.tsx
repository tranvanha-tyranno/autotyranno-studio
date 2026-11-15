import { Body, Card, Glyph, Kicker, Photo, Stage, Tag } from "./UI";
import { currency, useSemantic } from "./theme";
import type { SemanticShot } from "./types";
import { useCurrentFrame, interpolate } from "remotion";
import { clamp } from "./theme";

/** One stable work surface for the five very short narrated workday verbs. */
export const Workbench: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  const localFrame = useCurrentFrame();
  const { p, example: e } = useSemantic();
  const source = shot.scene === "product_facts",
    draft = shot.scene === "email_draft",
    check = shot.scene === "source_check",
    chat = shot.scene === "customer_reply",
    decision = shot.scene === "decision";
  return (
    <Stage shot={shot}>
      <div style={{ display: "flex", gap: 22, height: 605 }}>
        <Card
          style={{
            width: 430,
            padding: 27,
            borderWidth: source ? 3 : 1,
            borderColor: source ? p.accent : p.line,
          }}
        >
          <Kicker>HỒ SƠ GỐC · MẪU A</Kicker>
          {shot.asset ? (
            <div
              style={{
                position: "relative",
                height: 185,
                margin: "20px 0",
                overflow: "hidden",
                borderRadius: 9,
              }}
            >
              <Photo asset={shot.asset} />
            </div>
          ) : (
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 18,
                margin: "26px 0",
              }}
            >
              <Glyph kind="lamp" size={87} color={p.accent} />
              <Body style={{ fontSize: 31, fontWeight: 700 }}>
                Đèn bàn
                <br />
                Mẫu A
              </Body>
            </div>
          )}
          <Body
            style={{
              fontSize: 34,
              fontWeight: 700,
              marginTop: 25,
              background: source ? p.soft : undefined,
              padding: 8,
            }}
          >
            USB-C có dây
          </Body>
          <Tag good style={{ marginTop: 18, fontSize: 31 }}>
            Không pin
          </Tag>
          <div style={{ font: "700 34px Arial", marginTop: 27 }}>
            {currency(e.sourcePriceVND)}
          </div>
        </Card>
        <Card
          style={{
            width: 690,
            padding: 30,
            borderWidth: draft ? 3 : 1,
            borderColor: draft ? p.accent : p.line,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
            <Glyph kind="mail" size={44} color={p.accent} />
            <Kicker>EMAIL · NHÁP BAN ĐẦU</Kicker>
          </div>
          <div style={{ font: "23px Arial", color: p.muted, marginTop: 25 }}>
            Đến: khach@vidu.invalid
          </div>
          <Body style={{ fontSize: 35, fontWeight: 700, marginTop: 23 }}>
            Giới thiệu đèn bàn Mẫu A
          </Body>
          <Body style={{ fontSize: 35, lineHeight: 1.7, marginTop: 33 }}>
            {draft
              ? "Mời bạn xem đèn Mẫu A.".slice(
                  0,
                  Math.round(interpolate(localFrame, [0, 15], [10, 23], clamp)),
                )
              : "Mời bạn xem đèn Mẫu A."}
            <br />
            <span
              style={{
                color: check ? p.bad : p.ink,
                background: check ? p.bad + "22" : undefined,
              }}
            >
              Dùng không dây.
            </span>
            <br />
            Giá {currency(e.draftPriceVND)}.
          </Body>
          <Tag bad style={{ marginTop: 35 }}>
            Chưa kiểm tra · Chưa gửi
          </Tag>
        </Card>
        <Card
          style={{
            flex: 1,
            padding: 27,
            borderWidth: check || chat || decision ? 3 : 1,
            borderColor: check || chat || decision ? p.accent : p.line,
          }}
        >
          <Kicker>
            {chat
              ? "HỘI THOẠI KHÁCH"
              : decision
                ? "NGƯỜI DUYỆT: BẠN"
                : "CẦN LÀM TIẾP"}
          </Kicker>
          {chat ? (
            <>
              <div
                style={{
                  marginTop: 38,
                  padding: 24,
                  borderRadius: 10,
                  background: p.soft,
                  font: "38px Arial",
                }}
              >
                “Đèn có pin?”
              </div>
              <Tag bad style={{ marginTop: 30 }}>
                Chờ bạn trả lời
              </Tag>
            </>
          ) : decision ? (
            <>
              {["Sửa trả lời", "Không gửi", "Duyệt bản đúng"].map((t, i) => (
                <div
                  key={t}
                  style={{
                    padding: "25px 17px",
                    marginTop: 20,
                    border: `2px solid ${i === 1 ? p.accent : p.line}`,
                    borderRadius: 9,
                    font: "33px Arial",
                    display: "flex",
                    gap: 14,
                    alignItems: "center",
                  }}
                >
                  <div
                    style={{
                      width: 22,
                      height: 22,
                      border: `2px solid ${p.line}`,
                      borderRadius: "50%",
                      background: i === 1 ? p.accent : undefined,
                    }}
                  />
                  {t}
                </div>
              ))}
            </>
          ) : (
            <>
              {[
                ["Nguồn: có dây", check],
                ["Email: không dây", check],
                ["Giá cần đối chiếu", false],
              ].map(([t, active], index) => (
                <div
                  key={String(t)}
                  style={{
                    font: "31px Arial",
                    padding: "27px 0",
                    display: "flex",
                    alignItems: "center",
                    gap: 15,
                    borderBottom: `1px solid ${p.line}`,
                    color: active ? (index === 0 ? p.good : p.bad) : p.ink,
                  }}
                >
                  <Glyph
                    kind={active ? (index === 0 ? "check" : "cross") : "search"}
                    size={29}
                    color={active ? (index === 0 ? p.good : p.bad) : p.muted}
                  />
                  {t}
                </div>
              ))}
              <Tag bad style={{ marginTop: 30 }}>
                Chưa được gửi
              </Tag>
            </>
          )}
        </Card>
      </div>
    </Stage>
  );
};
