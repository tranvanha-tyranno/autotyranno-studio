import { useEffect, useMemo } from "react";
import { ThreeCanvas } from "@remotion/three";
import { useCurrentFrame } from "remotion";
import * as THREE from "three";
import { useSemantic } from "./theme";

const Lamp: React.FC<{ connected: boolean }> = ({ connected }) => {
  const f = useCurrentFrame();
  const { direction } = useSemantic();
  const cord = useMemo(
    () =>
      new THREE.CatmullRomCurve3([
        new THREE.Vector3(-0.4, -1.43, 0.2),
        new THREE.Vector3(-1.1, -1.45, 0.65),
        new THREE.Vector3(-1.5, -1.47, 0.8),
        new THREE.Vector3(-2.0, -1.48, 0.25),
        new THREE.Vector3(connected ? -2.35 : -1.94, -1.48, -0.05),
      ]),
    [connected],
  );
  const cordGeometry = useMemo(
    () => new THREE.TubeGeometry(cord, 48, 0.035, 10, false),
    [cord],
  );
  useEffect(() => () => cordGeometry.dispose(), [cordGeometry]);
  return (
    <group
      rotation={[0, -0.2 + Math.sin(f / 100) * 0.035, 0]}
      position={[0.35, 0, 0]}
    >
      <mesh position={[0, -1.4, 0]}>
        <cylinderGeometry args={[0.67, 0.75, 0.16, 48]} />
        <meshStandardMaterial
          color="#535b5b"
          metalness={0.65}
          roughness={0.3}
        />
      </mesh>
      <mesh position={[0, -0.3, 0]}>
        <cylinderGeometry args={[0.065, 0.065, 2.15, 20]} />
        <meshStandardMaterial
          color="#818c8e"
          metalness={0.75}
          roughness={0.3}
        />
      </mesh>
      <mesh position={[0.32, 0.93, 0]} rotation={[0, 0, -0.53]}>
        <cylinderGeometry args={[0.065, 0.065, 0.85, 20]} />
        <meshStandardMaterial
          color="#818c8e"
          metalness={0.75}
          roughness={0.3}
        />
      </mesh>
      <group position={[0.62, 1.23, 0]} rotation={[0.12, 0, -0.38]}>
        <mesh>
          <cylinderGeometry args={[0.34, 0.77, 0.58, 40]} />
          <meshStandardMaterial
            color="#eceee8"
            metalness={0.08}
            roughness={0.7}
          />
        </mesh>
        <mesh position={[0, -0.295, 0]} rotation={[Math.PI / 2, 0, 0]}>
          <circleGeometry args={[0.69, 40]} />
          <meshBasicMaterial
            color={connected ? "#fff3c6" : "#7b8c88"}
            side={THREE.DoubleSide}
          />
        </mesh>
      </group>
      <mesh geometry={cordGeometry}>
        <meshStandardMaterial
          color={direction === "long" ? "#28332f" : "#bdcfca"}
          roughness={0.6}
        />
      </mesh>
      <mesh position={[-2.96, -1.43, -0.06]}>
        <boxGeometry args={[0.7, 0.34, 0.45]} />
        <meshStandardMaterial
          color={direction === "long" ? "#50605b" : "#9aada5"}
        />
      </mesh>
      <group
        position={[connected ? -2.43 : -2.02, -1.48, -0.06]}
        rotation={[0, 0.2, 0]}
      >
        <mesh>
          <boxGeometry args={[0.34, 0.14, 0.22]} />
          <meshStandardMaterial color="#596966" />
        </mesh>
        <mesh position={[-0.19, 0, 0]}>
          <boxGeometry args={[0.1, 0.075, 0.16]} />
          <meshStandardMaterial
            color="#dbe4e1"
            metalness={0.7}
            roughness={0.2}
          />
        </mesh>
      </group>
    </group>
  );
};

/** The cable is an explanatory object, not a decorative orbit or a stock-unit claim. */
export const Lamp3D: React.FC<{
  width?: number;
  height?: number;
  connected?: boolean;
}> = ({ width = 830, height = 620, connected = true }) => (
  <ThreeCanvas
    width={width}
    height={height}
    camera={{ fov: 37, position: [0, 0.15, 6.9] }}
    gl={{ antialias: true, alpha: true }}
    style={{ position: "absolute", right: 0, top: 0 }}
  >
    <ambientLight intensity={1.5} />
    <directionalLight position={[2, 5, 4]} intensity={3} />
    <directionalLight position={[-3, 1, 4]} intensity={1.3} />
    <Lamp connected={connected} />
  </ThreeCanvas>
);

const TaskObject: React.FC<{ index: number; active: boolean }> = ({
  index,
  active,
}) => {
  const { p } = useSemantic();
  const texture = useMemo(() => {
    const canvas = document.createElement("canvas");
    canvas.width = 600;
    canvas.height = 400;
    const ctx = canvas.getContext("2d");
    if (!ctx) throw new Error("Task interface canvas unavailable");
    ctx.fillStyle = active ? p.soft : p.surface;
    ctx.fillRect(0, 0, 600, 400);
    ctx.fillStyle = p.muted;
    ctx.font = "bold 24px Arial";
    ctx.fillText(`0${index + 1} / MẪU A`, 38, 50);
    ctx.fillStyle = active ? p.accent : p.ink;
    ctx.font = "bold 51px Arial";
    ctx.fillText(["Tạo bản đầu", "Kiểm tra", "Quyết định"][index], 38, 338);
    ctx.strokeStyle = active ? p.accent : p.muted;
    ctx.lineWidth = 8;
    ctx.lineJoin = "round";
    ctx.lineCap = "round";
    if (index === 0) {
      ctx.strokeRect(190, 100, 220, 140);
      ctx.beginPath();
      ctx.moveTo(194, 105);
      ctx.lineTo(300, 185);
      ctx.lineTo(406, 105);
      ctx.stroke();
    } else if (index === 1) {
      ctx.strokeRect(205, 80, 180, 190);
      for (let i = 0; i < 3; i++) {
        ctx.beginPath();
        ctx.moveTo(230, 123 + i * 50);
        ctx.lineTo(244, 137 + i * 50);
        ctx.lineTo(267, 111 + i * 50);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(288, 125 + i * 50);
        ctx.lineTo(355, 125 + i * 50);
        ctx.stroke();
      }
    } else {
      ctx.beginPath();
      ctx.arc(300, 128, 39, 0, Math.PI * 2);
      ctx.stroke();
      ctx.beginPath();
      ctx.arc(300, 239, 70, Math.PI, 0);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(390, 175);
      ctx.lineTo(410, 195);
      ctx.lineTo(451, 150);
      ctx.stroke();
    }
    const t = new THREE.CanvasTexture(canvas);
    t.colorSpace = THREE.SRGBColorSpace;
    t.needsUpdate = true;
    return t;
  }, [active, index, p]);
  useEffect(() => () => texture.dispose(), [texture]);
  return (
    <group
      position={[
        (index - 1) * 3.35,
        active ? 0.1 : -0.12,
        active ? 0.28 : -0.2,
      ]}
      rotation={[0, (1 - index) * 0.09, 0]}
    >
      <mesh position={[0, 0, -0.085]}>
        <boxGeometry args={[3.16, 2.13, 0.12]} />
        <meshStandardMaterial
          color={active ? p.accent : p.line}
          metalness={0.25}
          roughness={0.6}
        />
      </mesh>
      <mesh>
        <planeGeometry args={[3.1, 2.07]} />
        <meshBasicMaterial map={texture} toneMapped={false} />
      </mesh>
    </group>
  );
};

export const TaskObjects3D: React.FC<{
  mode?: string;
  globalFrame: number;
}> = ({ mode, globalFrame }) => {
  const active =
    mode === "draft" ? 0 : mode === "review" ? 1 : mode === "decide" ? 2 : -1;
  return (
    <ThreeCanvas
      width={1720}
      height={590}
      camera={{ fov: 34, position: [0, 0.15, 8.4] }}
      gl={{ antialias: true, alpha: true }}
      style={{ position: "absolute", inset: 0 }}
    >
      <ambientLight intensity={1.4} />
      <directionalLight position={[0, 4, 6]} intensity={2} />
      <group rotation={[0, Math.sin(globalFrame / 240) * 0.012, 0]}>
        {[0, 1, 2].map((i) => (
          <TaskObject key={i} index={i} active={i === active} />
        ))}
        <mesh position={[0, -1.72, -0.35]}>
          <boxGeometry args={[9.7, 0.028, 0.035]} />
          <meshBasicMaterial color="#90b8b0" />
        </mesh>
        {[-3.35, 0, 3.35].map((x, i) => (
          <mesh key={x} position={[x, -1.72, -0.3]}>
            <sphereGeometry args={[i === active ? 0.075 : 0.045, 12, 10]} />
            <meshBasicMaterial color={i === active ? "#ef7851" : "#90b8b0"} />
          </mesh>
        ))}
      </group>
    </ThreeCanvas>
  );
};
