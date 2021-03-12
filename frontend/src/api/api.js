import axios from 'axios';

//export const test = 'http://172.22.6.109:8021';
//export const url  = 'http://172.22.6.109';
//export const test = 'http://127.0.0.1:8000';    //本地部署dev使用
export const test = 'http://wxweapp-api-test2.shenlanbao.com';	// 线上环境使用
//export const url  = 'http://172.22.7.87';
// 钉钉配置
export const dingConfig = params => { return axios.get(`${test}/api/user/dingConfig`, params).then(res => res.data); };
// 钉钉登录
export const dingLogin = params => { return axios.post(`${test}/api/user/dingConfig`, params).then(res => res.data); };
// 登录
export const requestLogin = params => { return axios.post(`${test}/api/user/login`, params).then(res => res.data); };
// 记录访客
export const recordVisitor = params => { return axios.post(`${test}/api/user/VisitorRecord`, params).then(res => res.data); };
// 获取项目
export const getProject = (headers, params) => {
    return axios.get(`${test}/api/project/project_list`, { params: params, headers:headers}).then(res => res.data); };
// 删除项目
export const delProject = (headers, params) => {
    return axios.post(`${test}/api/project/del_project`, params, {headers}).then(res => res.data); };
// 禁用项目
export const disableProject = (headers, params) => {
    return axios.post(`${test}/api/project/disable_project`, params, {headers}).then(res => res.data); };
// 启用项目
export const enableProject = (headers, params) => {
    return axios.post(`${test}/api/project/enable_project`, params, {headers}).then(res => res.data); };
// 修改项目
export const updateProject = (headers, params) => {
    return axios.post(`${test}/api/project/update_project`, params, {headers}).then(res => res.data); };
// 添加项目
export const addProject = (headers, params) => {
    return axios.post(`${test}/api/project/add_project`, params, {headers}).then(res => res.data); };
// 获取项目详情
export const getProjectDetail = (headers, params) => {
    return axios.get(`${test}/api/title/project_info`, { params: params, headers:headers}).then(res => res.data); };
// 获取测试地址列表
export const getHost = (headers, params) => {
    return axios.get(`${test}/api/global/host_total`, { params: params, headers:headers}).then(res => res.data); };
// 删除测试地址列表
export const delHost = (headers, params) => {
    return axios.post(`${test}/api/global/del_host`, params, {headers}).then(res => res.data); };
// 禁用测试地址列表
export const disableHost = (headers, params) => {
    return axios.post(`${test}/api/global/disable_host`, params, {headers}).then(res => res.data); };
// 启用测试地址列表
export const enableHost = (headers, params) => {
    return axios.post(`${test}/api/global/enable_host`, params, {headers}).then(res => res.data); };
// 修改测试地址列表
export const updateHost = (headers, params) => {
    return axios.post(`${test}/api/global/update_host`, params, {headers}).then(res => res.data); };
// 添加测试地址列表
export const addHost = (headers, params) => {
    return axios.post(`${test}/api/global/add_host`, params, {headers}).then(res => res.data); };
// 获取项目动态
export const getProjectDynamicList = (headers, params) => {
    return axios.get(`${test}/api/dynamic/dynamic`, { params: params, headers:headers}).then(res => res.data); };
// 获取项目成员
export const getProjectMemberList = (headers, params) => {
    return axios.get(`${test}/api/member/project_member`, { params: params, headers:headers}).then(res => res.data); };
// 获取发送邮件配置
export const getEmailConfigDetail = (headers, params) => {
    return axios.get(`${test}/api/member/get_email`, { params: params, headers:headers}).then(res => res.data); };
// 删除邮件配置
export const delEmailConfig = (headers, params) => {
    return axios.post(`${test}/api/member/del_email`, params, {headers}).then(res => res.data); };
// 添加邮件配置
export const addEmailConfig = (headers, params) => {
    return axios.post(`${test}/api/member/email_config`, params, {headers}).then(res => res.data); };
// 获取自动化测试结果
export const getTestResultList = (headers, params) => {
    return axios.get(`${test}/api/report/auto_test_report`, { params: params, headers:headers}).then(res => res.data); };
// 获取最近10次测试时间
export const getTestTenTime = (headers, params) => {
    return axios.get(`${test}/api/report/test_time`, { params: params, headers:headers}).then(res => res.data); };
// 获取最近10次测试比例结果
export const getTestTenResult = (headers, params) => {
    return axios.get(`${test}/api/report/lately_ten`, { params: params, headers:headers}).then(res => res.data); };
// 添加接口
export const addApiDetail = (headers, params) => {
    return axios.post(`${test}/api/api/add_api`, params, {headers}).then(res => res.data); };
// 获取接口分组列表
export const getApiGroupList = (headers, params) => {
    return axios.get(`${test}/api/api/group`, { params: params, headers:headers}).then(res => res.data); };
// 添加接口分组
export const addApiGroup = (headers, params) => { return axios.post(`${test}/api/api/add_group`, params, {headers}).then(res => res.data); };
// 修改接口分组
export const updateApiGroup = (headers, params) => {
    return axios.post(`${test}/api/api/update_name_group`, params, {headers}).then(res => res.data); };
// 删除接口分组
export const delApiGroup = (headers, params) => {
    return axios.post(`${test}/api/api/del_group`, params, {headers}).then(res => res.data); };

// 获取定时任务信息
export const getTimedTask = (headers, params) => {
    return axios.get(`${test}/api/task/timing_list`, { params: params, headers:headers}).then(res => res); };
// 添加账号来获取token
export const addLoginToken = (headers, params) => {
    return axios.post(`${test}/api/token/LoginToken`, params, {headers}).then(res => res.data); };
// 获取登录的账号名 密码
export const getLoginList = (headers, params) => {
    return axios.get(`${test}/api/token/listToken`, { params: params, headers:headers}).then(res => res.data); };
// 获取参数列表
export const get_parameter = (headers, params) => {
    return axios.get(`${test}/api/data/get_parameter`, { params: params, headers:headers}).then(res => res.data); };

// 获取接口列表
export const get_api_list = (headers, params) => {
    return axios.get(`${test}/api/automation/api_list`, { params: params, headers:headers}).then(res => res.data); };


// 添加数据库信息
export const addDataBase = (headers, params) => {
    return axios.post(`${test}/api/database/addData`, params, {headers}).then(res => res.data); };

// 获取数据库信息
export const getDataBase = (headers, params) => {
    return axios.get(`${test}/api/database/getData`, { params: params, headers:headers}).then(res => res.data); };


// 修改数据库信息
export const upDataBase = (headers, params) => {
    return axios.post(`${test}/api/database/updateData`, params, {headers}).then(res => res.data); };

// 删除数据库信息
export const delDataBase = (headers, params) => {
    return axios.post(`${test}/api/database/delDataBase`, params, {headers}).then(res => res.data); };

// 测试连接数据库
export const testConnection = (headers, params) => {
    return axios.get(`${test}/api/database/testConnection`, { params: params, headers:headers}).then(res => res.data); };

// 获取全局自定义变量
export const globalCustom = (headers, params) => {
    return axios.get(`${test}/api/custom/GetPublicVariable`, { params: params, headers:headers}).then(res => res.data); };