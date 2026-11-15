import {useCurrentFrame} from 'remotion';
import {Frame, colorFor, cue, font, rise} from './Shared';
import type {ChinaShot} from './types';

export const CompareScene: React.FC<{shot: ChinaShot}> = ({shot}) => {
  const frame = useCurrentFrame(), p = colorFor(shot), compare = shot.design?.comparison;
  if (!compare?.columns.length) throw new Error('c-compare needs comparison columns');
  const columns = compare.columns.slice(0, 3), width = 1700 / columns.length;
  return <Frame shot={shot} note={compare.note}>
    <div style={{position: 'absolute', left: 110, right: 110, top: 287, display: 'flex', gap: 24}}>
      {columns.map((col, i) => <div key={col.label} style={{width: width - 16, minHeight: 475, borderTop: `5px solid ${i === 1 ? p.accent : p.rule}`, padding: '25px 25px 30px', background: i === 1 ? p.soft : 'transparent', opacity: rise(frame, cue(shot, i, i * 18)), translate: `0 ${(1 - rise(frame, cue(shot, i, i * 18))) * 33}px`}}>
        <div style={{font: '700 21px Arial,sans-serif', letterSpacing: 2, color: p.quiet, marginBottom: 20}}>{col.label}</div>
        <div style={{fontFamily: font, fontSize: 45, fontWeight: 700, lineHeight: 1.14, maxWidth: 580}}>{col.title}</div>
        {col.value ? <div style={{fontFamily: font, fontSize: 66, color: p.accent, marginTop: 25, fontWeight: 700}}>{col.value}</div> : null}
        {col.body ? <div style={{font: '29px Arial,sans-serif', lineHeight: 1.4, marginTop: 24, color: p.quiet}}>{col.body}</div> : null}
        {(compare.rows ?? []).map(row => <div key={row.label} style={{paddingTop: 20, marginTop: 20, borderTop: `1px solid ${p.rule}`}}><div style={{font: '21px Arial,sans-serif', color: p.quiet}}>{row.label}</div><div style={{font: '700 28px Arial,sans-serif', marginTop: 8}}>{row.values[i]}</div></div>)}
      </div>)}
    </div>
  </Frame>;
};
