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
import { TaskObjects3D } from "./Objects3D";
import { ProductFacts } from "./EmailScenes";
import type { SemanticShot } from "./types";

export const Goal: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  const { p, example: e } = useSemantic();
  if (shot.mode === "product") return <ProductFacts shot={shot} />;
  const reader = shot.mode === "reader";
  return (
    <Stage shot={shot}>
      <Card
        style={{
          position: "absolute",
          left: 0,
          width: reader ? 1170 : 1540,
          minHeight: 520,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
          <Glyph
            kind={reader ? "person" : "document"}
            size={55}
            color={p.accent}
          />
          <Kicker>
            {reader ? "ĐIỀU NGƯỜI ĐỌC ĐANG CẦN" : "ĐIỀU CÓ THỂ CAM KẾT"}
          </Kicker>
        </div>
        {reader ? (
          <>
            <Body style={{ fontSize: 47, marginTop: 40 }}>
              “Tôi cần đèn dùng ở nơi
              <br />
              không có ổ cắm.”
            </Body>
            <div style={{ marginTop: 40 }}>
              <Tag bad>Không thể mặc định Mẫu A phù hợp</Tag>
            </div>
            <Body style={{ fontSize: 30, color: p.muted, marginTop: 25 }}>
              Hiểu nhu cầu trước khi viết lời chào hàng.
            </Body>
          </>
        ) : (
          <>
            <div
              style={{
                display: "flex",
                gap: 20,
                alignItems: "center",
                font: "42px Arial",
                marginTop: 42,
              }}
            >
              <Glyph kind="check" color={p.good} />
              <span>{e.sourceFeature}</span>
            </div>
            <div
              style={{
                display: "flex",
                gap: 20,
                alignItems: "center",
                font: "42px Arial",
                marginTop: 35,
              }}
            >
              <Glyph kind="cross" color={p.bad} />
              <span style={{ textDecoration: "line-through", color: p.bad }}>
                {e.unsupportedFeature}
              </span>
            </div>
            <Body style={{ fontSize: 32, marginTop: 40, color: p.muted }}>
              Có trong tài liệu gốc mới được đưa vào email.
            </Body>
          </>
        )}
      </Card>
      {reader ? (
        <Card
          style={{
            position: "absolute",
            right: 0,
            top: 35,
            width: 500,
            padding: 30,
          }}
        >
          <Kicker>THÔNG TIN GỐC</Kicker>
          <Glyph kind="lamp" size={125} color={p.accent} />
          <Body style={{ fontSize: 36, fontWeight: 700 }}>USB-C có dây</Body>
          <Tag bad style={{ marginTop: 26 }}>
            Không pin
          </Tag>
        </Card>
      ) : null}
    </Stage>
  );
};

export const Feedback: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  const { p } = useSemantic();
  const resolve = shot.mode === "resolve";
  const listen = shot.mode === "listen";
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
      <div style={{ width: shot.asset ? 1230 : 1640 }}>
        <Card>
          <Kicker>ĐIỀU KHÁCH HÀNG VỪA NÓI</Kicker>
          <div
            style={{
              display: "flex",
              gap: 25,
              marginTop: 26,
              alignItems: "center",
            }}
          >
            <Glyph kind="chat" size={60} color={p.accent} />
            <Body style={{ fontSize: 42 }}>
              “Nếu không có nguồn USB thì dùng được không?”
            </Body>
          </div>
        </Card>
        {listen ? (
          <Card
            style={{ marginTop: 28, marginLeft: 80, borderColor: p.accent }}
          >
            <Kicker>CẦN TRẢ LỜI</Kicker>
            <div
              style={{
                display: "flex",
                gap: 20,
                alignItems: "center",
                marginTop: 25,
              }}
            >
              <Glyph kind="chat" size={45} color={p.accent} />
              <Body style={{ fontSize: 38 }}>
                Đang chờ bạn xác minh nguồn điện.
              </Body>
            </div>
            <Tag bad style={{ marginTop: 28 }}>
              Chưa trả lời · Tiếp tục theo dõi
            </Tag>
          </Card>
        ) : (
          <Card
            style={{
              marginTop: 28,
              marginLeft: 80,
              borderColor: resolve ? p.good : p.line,
            }}
          >
            <Kicker>
              {resolve
                ? "TRẢ LỜI ĐÚNG VẤN ĐỀ"
                : "TRẢ LỜI LỊCH SỰ, NHƯNG CHƯA ĐỦ"}
            </Kicker>
            <Body style={{ fontSize: 38, marginTop: 23 }}>
              {resolve
                ? "Mẫu A dùng điện qua dây, không có pin. Mẫu này chưa phù hợp nhu cầu đó."
                : "“Cảm ơn anh/chị. Sản phẩm của chúng tôi rất tiện lợi.”"}
            </Body>
            <div style={{ marginTop: 25 }}>
              <Tag good={resolve} bad={!resolve}>
                {resolve
                  ? "Đã nối nhu cầu với thông tin gốc"
                  : "Chưa giải quyết nhu cầu dùng không dây"}
              </Tag>
            </div>
          </Card>
        )}
      </div>
    </Stage>
  );
};

export const TaskMap: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  const f = useCurrentFrame(),
    { p } = useSemantic();
  const names: Record<string, string> = {
    draft: "AI có thể tạo bản đầu.",
    review: "Bạn đối chiếu thông tin gốc.",
    decide: "Bạn chịu trách nhiệm trước khi gửi.",
    assignment: "Bạn giao phần nào? Giữ phần nào?",
    all: "Một email được hoàn thành qua cả ba bước.",
  };
  return (
    <Stage shot={shot}>
      <TaskObjects3D mode={shot.mode} globalFrame={shot.start + f} />
      {shot.mode === "assignment" ? (
        <div
          style={{
            position: "absolute",
            left: 115,
            right: 115,
            top: 12,
            display: "flex",
            justifyContent: "space-between",
          }}
        >
          <Tag good style={{ fontSize: 31 }}>
            AI hỗ trợ bản đầu
          </Tag>
          <Tag style={{ fontSize: 31 }}>Bạn kiểm tra nguồn và duyệt gửi</Tag>
        </div>
      ) : null}
      <div
        style={{
          position: "absolute",
          left: 50,
          right: 50,
          bottom: 0,
          textAlign: "center",
          font: "36px Arial",
          color: p.ink,
        }}
      >
        {names[shot.mode ?? "all"] ?? names.all}
      </div>
    </Stage>
  );
};

export const SendGate: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  const { p } = useSemantic();
  const pass = shot.mode === "reviewed";
  return (
    <Stage shot={shot}>
      <div style={{ display: "flex", gap: 28 }}>
        <Card style={{ width: 1110 }}>
          <Kicker>TRƯỚC KHI GỬI EMAIL</Kicker>
          {[
            "Đối chiếu tính năng với tài liệu gốc",
            "Kiểm tra giá và từng con số",
            "Giọng điệu phù hợp người đọc",
          ].map((t, i) => (
            <div
              key={t}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 22,
                borderBottom: `1px solid ${p.line}`,
                padding: "29px 0",
                font: "37px Arial",
              }}
            >
              <div
                style={{
                  width: 46,
                  height: 46,
                  border: `2px solid ${pass ? p.good : p.line}`,
                  borderRadius: 6,
                  display: "grid",
                  placeItems: "center",
                }}
              >
                {pass ? (
                  <Glyph kind="check" size={34} color={p.good} />
                ) : (
                  <span style={{ font: "25px Arial", color: p.muted }}>
                    {i + 1}
                  </span>
                )}
              </div>
              {t}
            </div>
          ))}
        </Card>
        <Card
          style={{
            flex: 1,
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            textAlign: "center",
            gap: 35,
          }}
        >
          <Glyph
            kind={pass ? "check" : "lock"}
            size={95}
            color={pass ? p.good : p.bad}
          />
          <div
            style={{
              font: "700 43px Arial",
              lineHeight: 1.2,
              color: pass ? p.good : p.bad,
            }}
          >
            {pass ? "ĐÃ KIỂM TRA" : "CHƯA ĐƯỢC GỬI"}
          </div>
          <Tag good={pass} bad={!pass}>
            {pass ? "Bạn quyết định" : "Bản nháp chưa phải kết quả"}
          </Tag>
        </Card>
      </div>
    </Stage>
  );
};

export const ReviewWork: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  const { p } = useSemantic();
  if (shot.mode === "checklist") return <NeedBridge shot={shot} />;
  return (
    <Stage shot={shot}>
      {shot.asset ? (
        <div
          style={{
            position: "absolute",
            right: 0,
            width: 630,
            top: 0,
            bottom: 0,
            borderRadius: 18,
            overflow: "hidden",
          }}
        >
          <Photo asset={shot.asset} />
        </div>
      ) : null}
      <Card style={{ width: shot.asset ? 1060 : 1550 }}>
        <Kicker>PHẦN VIỆC CHƯA BIẾN MẤT</Kicker>
        <div
          style={{
            display: "flex",
            gap: 22,
            alignItems: "center",
            marginTop: 38,
          }}
        >
          <Tag style={{ fontSize: 35 }}>AI: tạo nháp</Tag>
          <Glyph kind="arrow" color={p.accent} size={50} />
          <Tag style={{ fontSize: 35 }}>Bạn: kiểm tra</Tag>
        </div>
        <div
          style={{
            marginTop: 45,
            display: "flex",
            flexDirection: "column",
            gap: 23,
          }}
        >
          {[
            "Bản đầu: Dùng không dây",
            "Nguồn gốc: USB-C có dây · Không pin",
            "Cần sửa câu hứa trước khi gửi",
          ].map((t, index) => (
            <div
              key={t}
              style={{
                font: "36px Arial",
                textDecoration: index === 0 ? "line-through" : undefined,
                color: index === 0 ? p.bad : index === 1 ? p.good : p.ink,
                display: "flex",
                gap: 20,
                alignItems: "center",
              }}
            >
              <Glyph kind="search" color={p.accent} size={32} />
              {t}
            </div>
          ))}
        </div>
        <div style={{ marginTop: 35 }}>
          <Tag bad>Việc đã chuyển sang khâu kiểm tra</Tag>
        </div>
      </Card>
    </Stage>
  );
};

/** Reused across 'kiểm tra' and the 0.7s 'hiểu bối cảnh' clause. */
export const NeedBridge: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  const { p, example: e } = useSemantic();
  const context = shot.scene === "context";
  return (
    <Stage shot={shot}>
      <div style={{ display: "flex", gap: 24 }}>
        <Card style={{ flex: 1, borderColor: context ? p.accent : p.line }}>
          <Kicker>NHU CẦU CỦA KHÁCH</Kicker>
          <Body
            style={{
              fontSize: 45,
              lineHeight: 1.4,
              marginTop: 36,
              background: context ? p.soft : undefined,
              padding: 12,
            }}
          >
            “Dùng nơi không có ổ cắm.”
          </Body>
          <Tag bad style={{ marginTop: 32, fontSize: 29 }}>
            Cần dùng không dây
          </Tag>
        </Card>
        <Card style={{ flex: 1 }}>
          <Kicker>ĐỐI CHIẾU NGUỒN MẪU A</Kicker>
          <Body style={{ fontSize: 39, lineHeight: 1.5, marginTop: 32 }}>
            USB-C có dây · Không pin
            <br />
            {currency(e.sourcePriceVND)}
          </Body>
          <Tag good style={{ marginTop: 30 }}>
            Có căn cứ từ hồ sơ gốc
          </Tag>
        </Card>
        <Card style={{ flex: 1 }}>
          <Kicker>ĐIỀU CẦN NÓI RÕ</Kicker>
          <Body style={{ fontSize: 41, lineHeight: 1.4, marginTop: 32 }}>
            Cần nguồn qua cáp.
            <br />
            Mẫu này chưa phù hợp nhu cầu đó.
          </Body>
          <Tag good style={{ marginTop: 28 }}>
            Sửa trả lời trước khi gửi
          </Tag>
        </Card>
      </div>
    </Stage>
  );
};

export const TimeLog: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  const f = useCurrentFrame(),
    { p, example: e } = useSemantic();
  const total = e.writeMinutes + e.repairMinutes;
  const mode = shot.mode ?? "total";
  const amount =
    mode === "write"
      ? e.writeMinutes
      : mode === "repair"
        ? e.repairMinutes
        : total;
  return (
    <Stage shot={shot}>
      <div style={{ display: "flex", gap: 28 }}>
        <Card style={{ width: 690 }}>
          <Kicker>
            {mode === "write"
              ? "THỜI GIAN VIẾT"
              : mode === "repair"
                ? "THỜI GIAN KIỂM TRA + SỬA"
                : "TỔNG THỜI GIAN"}
          </Kicker>
          <div
            style={{
              font: "700 150px Bahnschrift,Arial",
              lineHeight: 1,
              marginTop: 38,
              color: mode === "write" ? p.good : p.bad,
            }}
          >
            {Math.round(
              interpolate(f, [0, 16], [amount * 0.75, amount], clamp),
            )}
            <span style={{ font: "38px Arial", marginLeft: 20 }}>phút</span>
          </div>
          <div style={{ marginTop: 43 }}>
            <Tag>DỮ LIỆU GIẢ ĐỊNH</Tag>
          </div>
          <Body style={{ fontSize: 32, color: p.muted, marginTop: 25 }}>
            Tính cả kiểm tra và sửa lỗi.
          </Body>
        </Card>
        <Card style={{ flex: 1 }}>
          <Kicker>SỔ THEO DÕI MỘT NHIỆM VỤ</Kicker>
          <div style={{ marginTop: 35 }}>
            {[
              ["Tự làm trước đây", e.baselineMinutes, p.muted],
              ["AI viết bản đầu", e.writeMinutes, p.good],
              ["Kiểm tra + sửa", e.repairMinutes, p.bad],
            ].map(([label, n, color]) => (
              <div key={String(label)} style={{ marginBottom: 24 }}>
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    font: "31px Arial",
                    marginBottom: 11,
                  }}
                >
                  <span>{label}</span>
                  <strong>
                    {mode === "write" && label === "Kiểm tra + sửa"
                      ? "Chờ đo"
                      : n + " phút"}
                  </strong>
                </div>
                <div
                  style={{
                    height: 23,
                    background: p.line + "55",
                    borderRadius: 4,
                  }}
                >
                  <div
                    style={{
                      height: "100%",
                      width: `${mode === "write" && label === "Kiểm tra + sửa" ? 0 : (Number(n) / Math.max(total, e.baselineMinutes)) * 100}%`,
                      background: String(color),
                      borderRadius: 4,
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              borderTop: `2px solid ${p.line}`,
              paddingTop: 20,
              font: "700 37px Arial",
            }}
          >
            <span>Tổng khi dùng AI</span>
            <span style={{ color: p.bad }}>
              {mode === "write"
                ? "Chưa có tổng"
                : `${e.writeMinutes} + ${e.repairMinutes} = ${total} phút`}
            </span>
          </div>
        </Card>
      </div>
    </Stage>
  );
};

export const QualityCompare: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  const frame = useCurrentFrame();
  const { p, example: e } = useSemantic();
  const complete = shot.mode === "completion";
  const total = shot.mode === "total";
  const speed = shot.mode === "speed";
  if (total || speed)
    return (
      <Stage shot={shot}>
        <div style={{ display: "flex", gap: 28 }}>
          <Card style={{ flex: 1 }}>
            <Kicker>
              {total ? "TỔNG THỜI GIAN TRƯỚC ĐÂY" : "MỘT THAO TÁC"}
            </Kicker>
            <Glyph kind="mail" size={110} color={p.accent} />
            <Body style={{ fontSize: 46, fontWeight: 700, marginTop: 20 }}>
              {total ? "Tự làm trọn nhiệm vụ" : "Viết bản nháp"}
            </Body>
            <div
              style={{
                font: "700 100px Bahnschrift,Arial",
                marginTop: 28,
                color: p.good,
              }}
            >
              {total ? e.baselineMinutes : e.writeMinutes}
              <span style={{ font: "35px Arial" }}> phút</span>
            </div>
            <Tag style={{ marginTop: 20 }}>
              {total ? "Mốc so sánh giả định" : "Nhanh hơn một phần"}
            </Tag>
            {total ? (
              <Body style={{ fontSize: 28, color: p.muted, marginTop: 22 }}>
                So cùng nhiệm vụ, cùng tiêu chuẩn đúng nguồn và nhu cầu.
              </Body>
            ) : null}
          </Card>
          <Card style={{ flex: 1 }}>
            <Kicker>TOÀN BỘ NHIỆM VỤ</Kicker>
            <div
              style={{
                display: "flex",
                gap: 20,
                alignItems: "center",
                marginTop: 35,
              }}
            >
              <Glyph kind="mail" size={65} />
              <Glyph kind="arrow" size={35} />
              <Glyph kind="search" size={65} />
              <Glyph kind="arrow" size={35} />
              <Glyph kind="check" size={65} />
            </div>
            <Body style={{ fontSize: 40, fontWeight: 700, marginTop: 38 }}>
              Viết + kiểm tra + sửa
            </Body>
            <div
              style={{
                font: "700 100px Bahnschrift,Arial",
                marginTop: 28,
                color: p.bad,
              }}
            >
              {e.writeMinutes + e.repairMinutes}
              <span style={{ font: "35px Arial" }}> phút</span>
            </div>
            <Tag bad>
              {total
                ? `${e.writeMinutes} phút nháp + ${e.repairMinutes} phút sửa`
                : "Chưa chắc năng suất cao hơn"}
            </Tag>
          </Card>
        </div>
      </Stage>
    );
  return (
    <Stage shot={shot}>
      <div style={{ display: "flex", gap: 28 }}>
        <Card style={{ flex: 1 }}>
          <Kicker>BẢN NHÁP BAN ĐẦU · TRÔNG HOÀN CHỈNH</Kicker>
          <div
            style={{
              display: "flex",
              gap: 16,
              alignItems: "center",
              marginTop: 25,
            }}
          >
            <Glyph kind="mail" color={p.accent} size={52} />
            <Body style={{ fontWeight: 700, fontSize: 39 }}>
              Email trình bày đẹp
            </Body>
          </div>
          <Body style={{ fontSize: 36, marginTop: 35, lineHeight: 1.8 }}>
            Chào anh/chị,
            <br />
            <Highlight bad>{e.unsupportedFeature}</Highlight>
            <br />
            Giá {currency(e.draftPriceVND)}.
          </Body>
          <Tag bad style={{ marginTop: 25 }}>
            Chưa đối chiếu nguồn
          </Tag>
        </Card>
        <Card style={{ flex: 1, borderColor: complete ? p.good : p.line }}>
          <Kicker>
            {complete ? "ĐÃ ĐỐI CHIẾU ĐỂ HOÀN THÀNH" : "ĐIỀU VẪN CẦN KIỂM TRA"}
          </Kicker>
          {complete ? (
            <>
              <Body style={{ fontSize: 34, lineHeight: 1.55, marginTop: 28 }}>
                Mẫu A dùng nguồn USB-C có dây, không có pin.
                <br />
                Giá {currency(e.sourcePriceVND)}.<br />
                Vì anh/chị cần dùng nơi không có ổ cắm, mẫu này chưa phù hợp.
              </Body>
              <Tag good style={{ marginTop: 27 }}>
                Đã trả lời nhu cầu · Khớp nguồn
              </Tag>
            </>
          ) : (
            [
              "Đúng tính năng: USB-C có dây",
              "Đúng giá: " + currency(e.sourcePriceVND),
              "Hiểu khách cần dùng ở đâu",
              "Bạn chịu trách nhiệm khi gửi",
            ].map((t, index) => (
              <div
                key={t}
                style={{
                  display: "flex",
                  gap: 18,
                  alignItems: "center",
                  font: "34px Arial",
                  padding: "25px 0",
                  borderBottom: `1px solid ${p.line}`,
                }}
              >
                {complete && frame >= index * 5 ? (
                  <Glyph kind="check" size={30} color={p.good} />
                ) : (
                  <div
                    style={{
                      width: 30,
                      height: 30,
                      border: `2px solid ${p.line}`,
                      borderRadius: 4,
                      flexShrink: 0,
                    }}
                  />
                )}
                {t}
              </div>
            ))
          )}
        </Card>
      </div>
    </Stage>
  );
};

export const Trial: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  const { p, example: e } = useSemantic();
  const mode = shot.mode ?? "choose";
  return (
    <Stage shot={shot}>
      <Card style={{ width: shot.asset ? 1080 : 1530, minHeight: 520 }}>
        <Kicker>THỬ MỘT NHIỆM VỤ CỤ THỂ</Kicker>
        {mode === "choose" ? (
          <>
            <div
              style={{
                display: "flex",
                gap: 22,
                alignItems: "center",
                marginTop: 43,
              }}
            >
              <Glyph kind="mail" size={75} color={p.accent} />
              <Body style={{ fontSize: 51, fontWeight: 700 }}>
                Nháp email giới thiệu Mẫu A
              </Body>
            </div>
            <div style={{ marginTop: 40 }}>
              <Tag>Chỉ chọn một việc · Kiểm tra được</Tag>
            </div>
            <div style={{ display: "flex", gap: 18, marginTop: 26 }}>
              <Tag style={{ opacity: 0.55 }}>Đối chiếu bảng</Tag>
              <Tag style={{ opacity: 0.55 }}>Trả lời khách</Tag>
            </div>
            <Cursor x={700} y={340} />
          </>
        ) : mode === "dummy_data" ? (
          <>
            <Body style={{ fontSize: 44, marginTop: 38 }}>
              Chỉ dùng bộ dữ liệu giả định.
            </Body>
            <div style={{ display: "flex", gap: 22, marginTop: 42 }}>
              <Tag good style={{ fontSize: 32 }}>
                Tên: Mẫu A
              </Tag>
              <Tag good style={{ fontSize: 32 }}>
                Khách: vidu.invalid
              </Tag>
            </div>
            <div style={{ marginTop: 35 }}>
              <Tag bad style={{ fontSize: 30 }}>
                <Glyph kind="lock" size={30} /> Không dùng dữ liệu khách hàng
                thật
              </Tag>
            </div>
          </>
        ) : mode === "compare" ? (
          <>
            <div style={{ display: "flex", gap: 24, marginTop: 35 }}>
              {["Bản gốc", "Kết quả AI", "Phần bạn sửa"].map((t, i) => (
                <div
                  key={t}
                  style={{
                    flex: 1,
                    padding: 25,
                    background: p.soft,
                    borderRadius: 10,
                  }}
                >
                  <Glyph
                    kind={i === 0 ? "document" : i === 1 ? "mail" : "search"}
                    size={65}
                    color={p.accent}
                  />
                  <Body
                    style={{ fontSize: 33, marginTop: 20, fontWeight: 700 }}
                  >
                    {t}
                  </Body>
                  <Body
                    style={{
                      fontSize: 28,
                      lineHeight: 1.4,
                      marginTop: 22,
                      color: i === 1 ? p.bad : p.ink,
                    }}
                  >
                    {i === 1 ? "Dùng không dây" : "USB-C có dây · Không pin"}
                    <br />
                    {currency(i === 1 ? e.draftPriceVND : e.sourcePriceVND)}
                  </Body>
                  {i === 2 ? (
                    <div
                      style={{
                        font: "25px Arial",
                        lineHeight: 1.4,
                        color: p.good,
                        marginTop: 19,
                      }}
                    >
                      Nhu cầu không ổ cắm:
                      <br />
                      Mẫu này chưa phù hợp.
                    </div>
                  ) : null}
                </div>
              ))}
            </div>
            <Body style={{ fontSize: 34, marginTop: 38 }}>
              So từng tính năng, con số và cách trả lời.
            </Body>
          </>
        ) : (
          <>
            {[
              "Đúng tính năng ghi trong nguồn",
              "Đúng giá và đơn vị",
              "Trả lời đúng nhu cầu khách",
              "Không còn lỗi chưa kiểm tra",
            ].map((t) => (
              <div
                key={t}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 20,
                  font: "38px Arial",
                  padding: "23px 0",
                  borderBottom: `1px solid ${p.line}`,
                }}
              >
                <div
                  style={{
                    width: 32,
                    height: 32,
                    border: `2px solid ${p.line}`,
                    borderRadius: 4,
                    flexShrink: 0,
                  }}
                />
                {t}
              </div>
            ))}
          </>
        )}
      </Card>
      {shot.asset ? (
        <div
          style={{
            position: "absolute",
            right: 0,
            width: 590,
            top: 0,
            bottom: 0,
            borderRadius: 18,
            overflow: "hidden",
          }}
        >
          <Photo asset={shot.asset} />
        </div>
      ) : null}
    </Stage>
  );
};

export const QualityGate: React.FC<{ shot: SemanticShot }> = ({ shot }) => {
  const { p, example: e } = useSemantic();
  const pass = shot.mode === "pass";
  const unverifiable = shot.phrase.includes("không kiểm tra");
  if (pass)
    return (
      <Stage shot={shot}>
        <Card style={{ width: 1620, minHeight: 560 }}>
          <Kicker>ĐIỀU KIỆN: BẠN KIỂM TRA ĐƯỢC</Kicker>
          <div style={{ display: "flex", gap: 26, marginTop: 34 }}>
            {[
              [
                "Tính năng",
                "Nguồn: USB-C có dây / Không pin",
                "Email đã sửa: có dây, không pin",
              ],
              [
                "Giá",
                "Nguồn: " + currency(e.sourcePriceVND),
                "Email đã sửa: " + currency(e.sourcePriceVND),
              ],
              [
                "Nhu cầu",
                "Khách: không có ổ cắm",
                "Trả lời: Mẫu này chưa phù hợp",
              ],
            ].map(([a, b, c]) => (
              <div
                key={a}
                style={{
                  flex: 1,
                  padding: 24,
                  border: `1px solid ${p.good}`,
                  borderRadius: 10,
                }}
              >
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 15,
                    font: "700 32px Arial",
                  }}
                >
                  <Glyph kind="check" color={p.good} size={31} />
                  {a}
                </div>
                <Body style={{ fontSize: 29, lineHeight: 1.45, marginTop: 24 }}>
                  {b}
                  <br />
                  {c}
                </Body>
              </div>
            ))}
          </div>
          <Tag good style={{ marginTop: 34, fontSize: 30 }}>
            Chỉ giữ cách làm khi xác minh được từng tiêu chí
          </Tag>
        </Card>
      </Stage>
    );
  return (
    <Stage shot={shot}>
      <Card style={{ width: 1560, minHeight: 520 }}>
        <div style={{ display: "flex", gap: 22, alignItems: "center" }}>
          <Glyph
            kind={pass ? "check" : "search"}
            size={60}
            color={pass ? p.good : p.bad}
          />
          <Kicker>
            {pass
              ? "ĐÃ KIỂM SOÁT CHẤT LƯỢNG"
              : unverifiable
                ? "CHƯA ĐỦ CĂN CỨ XÁC MINH"
                : "LỖI CÒN SÓT"}
          </Kicker>
        </div>
        <div style={{ display: "flex", gap: 30, marginTop: 42 }}>
          <div style={{ flex: 1, font: "40px Arial", lineHeight: 1.7 }}>
            <div>
              {unverifiable
                ? "Cam kết chưa có nguồn xác minh"
                : pass
                  ? "USB-C có dây"
                  : e.unsupportedFeature}
            </div>
            <div>
              {unverifiable
                ? "☐ Chưa kiểm được"
                : currency(pass ? e.sourcePriceVND : e.draftPriceVND)}
            </div>
          </div>
          <div style={{ width: 1, background: p.line }}>
            <span />
          </div>
          <div style={{ flex: 1 }}>
            <Body
              style={{
                fontSize: 41,
                fontWeight: 700,
                color: pass ? p.good : p.bad,
              }}
            >
              {pass
                ? "Khớp nguồn và kiểm tra được"
                : unverifiable
                  ? "Chặn duyệt · Chưa gửi"
                  : "Chưa đạt yêu cầu"}
            </Body>
            <Body style={{ fontSize: 33, marginTop: 25, color: p.muted }}>
              {pass
                ? "Bạn biết vì sao kết quả đúng."
                : unverifiable
                  ? "Chưa có nguồn đối chiếu cho lời cam kết."
                  : "Tính năng và con số chưa khớp bản gốc."}
            </Body>
            <Tag good={pass} bad={!pass} style={{ marginTop: 28 }}>
              {pass
                ? "Có thể quyết định dùng"
                : "Sửa cách giao việc · Chưa gửi"}
            </Tag>
          </div>
        </div>
      </Card>
    </Stage>
  );
};
