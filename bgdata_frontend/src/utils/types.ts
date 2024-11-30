export type PaperContent = {
  title: string;
  abstract: string;
  year: string;
  category: string;
  refCount: number;
}

/**
 * USER_MODULE: 用户模块
 */

export type UserInfo = {
  username: string;
  premium: boolean;
  token: string;
}

/**
 * PAPER_MODULE: 论文模块
 */

export type Text = {
  text: string;
}

/**
 * SERVICE_MODULE: 服务模块
 */

export type SearchResult = {
  idList: number[];
  totalPage: number;
}

/**
 * GRAPH: 图模块
 */

export type GraphNode = {
  id: string;
  name: string;
  color: string;
}

export type GraphLine = {
  from: string;
  to: string;
}