import {Scene} from '../Scene';
import type {Chapter} from '../types';
export const PortfolioScene:React.FC<{chapter:Chapter}>=({chapter})=><Scene chapter={chapter}/>;
