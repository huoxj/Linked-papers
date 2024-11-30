import  {get} from "@/utils/request";
import {PAPER_MODULE} from "@/api/_prefix";

export const reqPaperAbstract = (id: number) => {
  return get<string>(`${PAPER_MODULE}/abstract`, {id})
}

export const reqPaperTitle = (id: number) => {
  return get<string>(`${PAPER_MODULE}/title`, {id})
}

export const reqPaperReference = (id: number) => {
  return get<number[]>(`${PAPER_MODULE}/reference`, {id})
}

export const reqPaperYear = (id: number) => {
  return get<string>(`${PAPER_MODULE}/year`, {id})
}

export const reqPaperCategory = (id: number) => {
  return get<string>(`${PAPER_MODULE}/category`, {id})
}

export const reqPaperRelated = (id: number) => {
  return get<number[]>(`${PAPER_MODULE}/related`, {id})
}

export const reqPaperSameCategory = (id: number) => {
  return get<number[]>(`${PAPER_MODULE}/samecategory`, {id})
}

export const reqPaperContentBrief = (id: number) => {
  const reqTitle = reqPaperTitle(id),
        reqAbstract = reqPaperAbstract(id),
        reqYear = reqPaperYear(id),
        reqCategory = reqPaperCategory(id),
        reqRefCount = reqPaperReference(id);
  return Promise.all([reqTitle, reqAbstract, reqYear, reqCategory, reqRefCount])
}