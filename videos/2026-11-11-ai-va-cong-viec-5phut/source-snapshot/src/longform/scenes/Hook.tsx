import {Scene} from '../Scene';
import type {Chapter} from '../types';
export const HookScene:React.FC<{chapter:Chapter}>=({chapter})=><Scene chapter={chapter}/>;
