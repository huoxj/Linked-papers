import {post} from "@/utils/request";
import {USER_MODULE} from "@/api/_prefix";
import type {UserInfo} from "@/utils/types";

export const reqLogin = (email: string, password: string) => {
    return post<UserInfo>(`${USER_MODULE}/login`, {email, password});
}

// export const reqRegister = (registerInfo: UserInfo) => {
//   return post<UserInfo>(`${USER_MODULE}/register`, registerInfo);
// }
export const reqRegister = (email: string, username: string, password: string, premium: boolean) => {
    return post<boolean>(`${USER_MODULE}/register`, {email, username, password, premium});
}
