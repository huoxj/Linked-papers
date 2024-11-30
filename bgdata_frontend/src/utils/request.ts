import axios from 'axios'

const service = axios.create()

function hasToken() {
    return !(sessionStorage.getItem('token') == '')
}

service.interceptors.request.use(
    config => {
        if(hasToken()) {
            config.headers['token'] = sessionStorage.getItem('token')
        }
        return config
    },
    error => {
        console.log(error);
        return Promise.reject();
    }
)

service.interceptors.response.use(
    response => {
        if (response.status === 200) {
            return response;
        } else {
            return Promise.reject();
        }
    },
    error => {
        console.log(error);
        return Promise.reject();
    }
)

export type Response<T> = {
  status: number,
  data: T
}

function get<T>(url: string, params?: {}): Promise<Response<T>> {
  return service.get(url, {params}).then(res => {return res.data});
}

function post<T>(url: string, data?: {}, headers?: {}): Promise<Response<T>> {
  return service.post(url, data, {headers}).then(res => {return res.data});
}

export { get, post }