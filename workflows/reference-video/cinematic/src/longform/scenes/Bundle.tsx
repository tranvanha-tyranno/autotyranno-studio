import {Scene} from '../Scene';
import type {Chapter} from '../types';
export const BundleScene:React.FC<{chapter:Chapter}>=({chapter})=><Scene chapter={chapter}/>;
