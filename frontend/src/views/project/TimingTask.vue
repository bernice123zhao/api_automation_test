<template>
        <!-- 账号列表 -->
    <el-row class="dynamic-manage">
        <el-col :span="24">
                <el-table :data="tableData" stripe style="width: 100%" v-loading="listLoading">
                    <el-table-column prop="project_name" label="项目名称" min-width="10%"></el-table-column>
                    <el-table-column prop="name" label="定时名称" min-width="10%"></el-table-column>
                    <el-table-column prop="host_name" label="Host" min-width="10%"></el-table-column>
                    <el-table-column prop="next_run_time" label="下次执行时间" min-width="20%"></el-table-column>
                    <el-table-column prop="type" label="类型" min-width="10%">
                        <template slot-scope="scope">
                            <span v-show="scope.row.type==='timing'">定时</span>
                            <span v-show="scope.row.type==='circulation'">间隔</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="frequency" label="参数" min-width="10%"></el-table-column>
                </el-table>
                <!--工具条-->
                <el-col :span="24" class="toolbar">
                    <el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="20"
                                   :page-count="total" style="float:right;">
                    </el-pagination>
                </el-col>
        </el-col>
    </el-row>
</template>

<script>
    import {getTimedTask} from '../../api/api';

    export default {
        name: "TimingTask",
        data() {
            return {
                currentPage: 1,
                pagesize: 20,
                tableData:[],
            }
        },
        mounted() {
            this.getTimimg()
        },
        methods: {
            //获取列表信息
            getTimimg() {
                // 并且响应成功以后会执行then方法中的回调函数37c907e4adfef03a443ea001fea49b29f2a903b5
                // let headers = {Authorization: 'Token ' + sessionStorage.getItem('token')}
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                };
                let params = {
                    page: this.page,
                    pagesize: this.pagesize,
                    name: '',
                };
                getTimedTask(headers, params).then(res => {
                    // result是所有的返回回来的数据
                    // //console.log(res.data);
                    this.total = res.data.data.total;
                    this.tableData = res.data.data.data;
                });
            }
        }
    }
</script>

<style scoped>

</style>