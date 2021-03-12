<template>
    <div>
        <div>
            <el-button type="primary" @click.native="taskVShow=true">
                <div>定时任务</div>
            </el-button>
        </div>
        <template>
            <el-dialog title="定时计划" :visible.sync="taskVShow" :close-on-click-modal="false"
                       style="width: 70%; left: 15%">
                <el-form ref="form" :model="form" label-width="100px">
                    <el-row :gutter="24">
                        <el-col :span="13">
                            <el-form-item label="任务名称：" prop="name">
                                <el-input v-model.trim="form.name" placeholder="请输入任务名称"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-form-item label="类型：" prop="type">
                        <el-select v-model="form.type" placeholder="请选择">
                            <el-option v-for="item in type" :key="item.value" :label="item.label"
                                       :value="item.value"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="公式模板：" prop="timingtemplate">
                        <el-select v-model="form.timingtemplate" placeholder="请选择" v-if="form.type === 'timing'">
                            <el-option v-for="item in timingtemplate" :key="item.value" :label="item.label"
                                       :value="item.value">
                            </el-option>
                        </el-select>
                        <el-select v-model="form.circulatemplate" placeholder="请选择" v-if="form.type === 'circulation'">
                            <el-option v-for="item in circulatemplate" :key="item.value" :label="item.label"
                                       :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="公式" prop='timingtemplate'>
                        <el-input type="textarea" :rows="4" v-model.trim="form.timingtemplate"
                                  v-if="form.type === 'timing'"
                                  placeholder="可参考下方定时公式"></el-input>
                        <el-input type="textarea" :rows="4" v-model.trim="form.circulatemplate"
                                  v-if="form.type === 'circulation'"
                                  placeholder="可参考下方间隔公式"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" :loading="editLoading" @click.native="addtimingSubmit">创建</el-button>
                        <el-tooltip class="item" placement="top">
                            <div slot="content" class="timiming">间隔调度，参数如下：<br/>
                                weeks (int) – 间隔几周 <br/>
                                days (int) – 间隔几天 <br/>
                                hours (int) – 间隔几小时 <br/>
                                minutes (int) – 间隔几分钟 <br/>
                                seconds (int) – 间隔多少秒 <br/>
                                start_date (datetime|str) – 开始日期 <br/>
                                end_date (datetime|str) – 结束日期 <br/>
                                举个栗子：<br/> 每两个小时执行
                                <br/> 公式:hours=2
                            </div>
                            <el-button>间隔公式</el-button>
                        </el-tooltip>
                        <el-tooltip class="item" placement="top">
                            <div slot="content" class="timiming">定时调度，参数如下：<br/>
                                year (int|str) – 年，4位数字 <br/>
                                month (int|str) – 月 (范围1-12) <br/>
                                day (int|str) – 日 (范围1-31) <br/>
                                week (int|str) – 周 (范围1-53) <br/>
                                day_of_week (int|str) – 周内第几天或者星期几 (范围0-6 或者 mon,tue,wed,thu,fri,sat,sun) <br/>
                                hour (int|str) – 时 (范围0-23) <br/>
                                minute (int|str) – 分 (范围0-59) <br/>
                                second (int|str) – 秒 (范围0-59) <br/>
                                start_date (datetime|str) – 最早开始日期(包含) <br/>
                                end_date (datetime|str) – 最晚结束时间(包含) <br/>
                                举个栗子：<br/>
                                # job_function将会在6,7,8,11,12月的第3个周五的1,2,3点运行<br/>
                                sched.add_job(job_function, 'cron', month='6-8,11-12', day='3rd fri', hour='0-3')<br/>
                                # 截止到2016-12-30 00:00:00，每周一到周五早上五点半运行job_function<br/>
                                sched.add_job(job_function, 'cron', day_of_week='mon-fri', hour=5, minute=30,
                                end_date='2016-12-31')<br/>
                            </div>
                            <el-button>定时公式</el-button>
                        </el-tooltip>
                    </el-form-item>
                </el-form>
            </el-dialog>
        </template>
    </div>
</template>

<script>
    export default {
        name: "timing",
        data() {
            return {
                timingtemplate: [
                    {value: "hour=9, minute=8, second=50"},
                    {value: "month='6-8,11-12', day='3rd fri', hour='0-3'"},
                    {value: "day_of_week='mon-fri', hour=5, minute=30, end_date='2016-12-31'"},
                ],
                circulatemplate: [{value: "hours=9"}, {value: "minutes=9"}, {value: "seconds=9"},
                    {value: "days=9"}, {value: "weeks=9"}],
                taskVShow: false,
                editLoading: false,
                type: [{value: "circulation", label: "间隔"},
                    {value: "timing", label: "定时"},],
                form: {
                    name: "",
                    type: "timing",
                    frequency: "",
                    unit: "m",
                    time: "",
                    timeArray: [],
                    Host: "",
                    parameters: "",
                    template: ''
                },
            }
        },
        methods: {
            //添加定时任务
            addtimingSubmit: function () {
                this.$refs.form.validate((valid) => {
                    let self = this;
                    this.$confirm('确认提交吗？', '提示', {}).then(() => {
                        var url = test + "/api/task/timing";
                        if (self.form.type === 'timing') {
                            var parameterTemplates = self.form.timingtemplate
                        } else {
                            var parameterTemplates = self.form.circulatemplate
                        }
                        let params = {
                            project_id: Number(self.$route.params.project_id),
                            parameters: parameterTemplates,
                            timingType: self.form.type,
                            host_id: Number(self.form.Host),
                        };
                        let headers = {
                            Authorization: 'Token ' + sessionStorage.getItem('token'),
                            'Content-Type': 'application/json',
                        };
                        axios.post(url, params, {
                                headers: headers
                            }
                        ).then(res => {
                            let {msg, code, data} = res.data;
                            self.addLoading = false;

                            if (code === '999999') {
                                // self.total = data.total;
                                self.$message({
                                    message: '添加成功',
                                    center: true,
                                    type: 'success'
                                });
                                self.$refs['form'].resetFields();
                                self.taskVShow = false;
                                self.getProjectList()
                            } else if (code === '999997') {
                                self.$message.error({
                                    message: msg,
                                    center: true,
                                })
                            } else {
                                self.$message.error({
                                    message: msg,
                                    center: true,
                                });
                                self.$refs['form'].resetFields();
                                self.taskVShow = false;
                                self.getProjectList()
                            }
                        })
                    });
                });
            },
        }
    }
</script>

<style scoped>

</style>