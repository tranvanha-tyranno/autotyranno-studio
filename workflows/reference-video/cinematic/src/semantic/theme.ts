import { createContext, useContext } from "react";
import type { SemanticDirection, SemanticExample } from "./types";
export const exampleDefaults: SemanticExample = {
  productName: "Đèn bàn Mẫu A",
  sourceFeature: "Nguồn USB-C có dây · Không pin",
  unsupportedFeature: "Dùng không dây",
  sourcePriceVND: 1200000,
  draftPriceVND: 120000,
  baselineMinutes: 12,
  writeMinutes: 2,
  repairMinutes: 13,
};
export const palettes = {
  long: {
    bg: "#eae4d8",
    surface: "#fffdf7",
    ink: "#18201f",
    muted: "#646b67",
    accent: "#d95132",
    soft: "#f4ddd3",
    line: "#c7c9bf",
    good: "#197667",
    bad: "#b84436",
    heading: "Bahnschrift,Arial,sans-serif",
    shadow: "0 22px 70px rgba(26,35,31,.16)",
  },
  hidden: {
    bg: "#081923",
    surface: "#102b37",
    ink: "#f1efe4",
    muted: "#a3b6ba",
    accent: "#86cac0",
    soft: "#1b3d46",
    line: "#36545e",
    good: "#9ed5b4",
    bad: "#ffb199",
    heading: "Times New Roman,Arial,serif",
    shadow: "0 28px 80px rgba(0,0,0,.33)",
  },
};
export const SemanticContext = createContext({
  direction: "long" as SemanticDirection,
  example: exampleDefaults,
  actionFrame: 0,
});
export const useSemantic = () => {
  const ctx = useContext(SemanticContext);
  return { ...ctx, p: palettes[ctx.direction] };
};
export const currency = (n: number) => n.toLocaleString("vi-VN") + " ₫";
export const clamp = {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
} as const;
