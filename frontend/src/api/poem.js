import request from './index'

/**
 * 通用检索（分页）
 * @param {string} q 关键词
 * @param {number} page 页码
 * @param {number} pageSize 每页条数
 * @returns {{ items: Array, total: number, page: number, page_size: number }}
 */
export function searchPoems(q, page = 1, pageSize = 18) {
  return request.get('/search', { params: { q, page, page_size: pageSize } })
}

/**
 * 获取所有诗词列表（分页）
 * @param {number} page 页码
 * @param {number} pageSize 每页条数
 * @returns {{ items: Array, total: number, page: number, page_size: number }}
 */
export function getAllPoems(page = 1, pageSize = 18) {
  return request.get('/poems', { params: { page, page_size: pageSize } })
}

/**
 * 获取诗词简洁详情
 * @param {string} id 诗词ID
 */
export function getPoemById(id) {
  return request.get(`/poems/${id}`)
}

/**
 * 获取诗词鉴赏详情（含原文、译文、赏析）
 * @param {string} id 诗词ID
 */
export function getPoemDetail(id) {
  return request.get(`/poem/${id}/detail`)
}

/**
 * 按作者名检索诗词（分页）
 * @param {string} name 作者名
 * @param {number} page 页码
 * @param {number} pageSize 每页条数
 * @returns {{ items: Array, total: number, page: number, page_size: number }}
 */
export function getPoemsByAuthor(name, page = 1, pageSize = 18) {
  return request.get(`/authors/${encodeURIComponent(name)}/poems`, { params: { page, page_size: pageSize } })
}
