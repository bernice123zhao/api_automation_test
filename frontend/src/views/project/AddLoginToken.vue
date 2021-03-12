<template>
    <!--列表-->
    <el-row class="member-manage">
        <p style="color:#999">*注<strong>: </strong>登录平台后，系统会自动根据以下信息自动获取token</p>
        <div style="margin-bottom: 20px;font-size: 20px">
            <div>
                <div style="display: inline">获取Token信息： </div>
                <i class="el-icon-edit" style="cursor:pointer;display: inline" @click="editFormVisible=true"></i>&nbsp;&nbsp;
            </div>
        </div>
        <el-dialog title="编辑" :visible.sync="editFormVisible" :close-on-click-modal="false" style="width: 60%; left: 20%">
		    <el-form :model="edmitMemberData" label-width="100px"   ref="editForm">
                <el-form-item label="用户名:" prop="username">
                    <el-input v-model.trim="edmitMemberData.username" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="密码:" prop="password">
                    <el-input v-model.trim="edmitMemberData.password" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="登录地址:" prop="url">
                    <el-input v-model.trim="edmitMemberData.url" auto-complete="off"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="editFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
            </div>
		</el-dialog>
        <el-col :span="24">
            <el-table :data="memberData" highlight-current-row  style="width: 100%;">
                <el-table-column prop="username" label="账号" min-width="8%" sortable>
                </el-table-column>
                <el-table-column prop="password" label="密码" min-width="8%" sortable>
                </el-table-column>
                <el-table-column prop="url" label="登录地址" min-width="30%" sortable>
                </el-table-column>
                <el-table-column prop="value" label="Token" min-width="30%" sortable>
                </el-table-column>
                <el-table-column prop="LastUpdateTime" label="上次更新时间" min-width="6%" sortable>
                </el-table-column>
            </el-table>
            <!--工具条-->
            <el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="20" :page-count="total" style="float:right;">
            </el-pagination>
        </el-col>
    </el-row>
</template>

<script>
    import { addLoginToken,getLoginList} from "../../api/api";
    export default {
        data() {
            return {
                memberData: [],
                edmitMemberData:{},
                total: 0,
                page: 1,
                listLoading: false,
                reportFrom: "",
                editFormVisible: false,//编辑界面是否显示
                editLoading: false,
                editFormRules: {
                    reportFrom: [
                        { required: true, message: '请输入发送人', trigger: 'blur' },
                        { min: 1, max: 100, message: '长度在 1 到 100 个字符', trigger: 'blur' }
                    ],
                    mailUser: [
                        { required: true, message: '请输入用户名', trigger: 'blur' },
                        { min: 1, max: 100, message: '长度在 1 到 100 个字符', trigger: 'blur' }
                    ],
                    mailPass: [
                        { required: true, message: '请输入口令', trigger: 'blur' },
                        { min: 1, max: 100, message: '长度在 1 到 100 个字符', trigger: 'blur' }
                    ],
                    mailSmtp: [
                        { required: false, message: '请输入邮件服务器', trigger: 'blur' },
                        { min: 1, max: 100, message: '长度在 1 到 100 个字符', trigger: 'blur' }
                    ]
                },
                //编辑界面数据
                editForm: {
                },
            }
        },
        methods: {
            handleCurrentChange(val) {
                this.page = val;
                this.getProjectMember()
            },
            // 获取成员列表
            getProjectMember() {
                this.listLoading = true;
                let self = this;
                let params = {
                    project_id: this.$route.params.project_id,
                };
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                };
                getLoginList(headers, params).then(_data => {
                    let {msg, code, data} = _data;
                           console.log(data )
                    self.listLoading = false;
                    if (code === '999999') {
                        self.memberData = data
                        if (self.memberData.length>0) {
                            this.edmitMemberData=self.memberData[0]
                        }
                    }
                    else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                })
            },
            editSubmit: function () {
                let self = this;
                this.$refs.editForm.validate((valid) => {
                    if (valid) {
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.editLoading = true;
                            //NProgress.start();
                            let params = {
                                project: Number(this.$route.params.project_id),
                                username: this.edmitMemberData.username,
                                password: this.edmitMemberData.password,
                                url: this.edmitMemberData.url,
                            };
                            let headers = {
                                "Content-Type": "application/json",
                                Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                            };
                            addLoginToken(headers, params).then(_data => {
                                let {msg, code, data} = _data;
                                self.editLoading = false;
                                if (code === '999999') {
                                    self.$message({
                                        message: '修改成功',
                                        center: true,
                                        type: 'success'
                                    });
                                    self.$refs['editForm'].resetFields();
                                    self.editFormVisible = false;
                                    this.getProjectMember()
                                } else if (code === '999997'){
                                    self.$message.error({
                                        message: msg,
                                        center: true,
                                    })
                                } else {
                                    self.$message.error({
                                        message: msg,
                                        center: true,
                                    })
                                }
                            })
                        });
                    }
                });
            },
        },
        mounted() {
            this.getProjectMember();

        }
    }
</script>

<style lang="scss" scoped>
    .member-manage {
        margin: 35px;
    }
</style>