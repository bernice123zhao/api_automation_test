<template>
  <div>
    <el-container>
      <el-aside class="bgwh" v-loading="treeLoading">
        <div class="pt15 pl15">(组织编制数/自身及下级组织编制合计)</div>
        <div class="tc">
          <el-form class="bgwh radius p15" inline size="small">
            <el-input @keyup.native="getRemoteFollow" placeholder="请输入内容" v-model="searchOrgKey">
              <i class="el-input__icon el-icon-search" slot="prefix"></i>
            </el-input>
          </el-form>
        </div>
        <div class="mt5 pl10" style="color:#555">轻轻集团</div>
        <el-tree
          :load="loadNode"
          :props="treeProps"
          @node-click="handleNodeClick"
          accordion
          highlight-current
          lazy
          node-key="id"
          ref="tree"
        >
          <div class="custom-tree-node" slot-scope="{ node, data }">
            <div>
              <span class="el-icon-star-on" v-if="data.organizationType===0 &
              data.isHasOrganization===true"></span>
              <span class="el-icon-moon" v-if="data.organizationType===10 &
              data.isHasOrganization===true"></span>
              <span class="el-icon-s-custom" v-if="data.isHasOrganization===undefined"></span>
              <span style="color: #888888" v-if="data.isHasOrganization===false ||
              data.isHasOrganization===undefined">{{ node.label }}</span>
              <span v-if="data.isHasOrganization===true">{{ node.label }}</span>
              <span v-if="data.isOrg">({{data.positionCount}}/
                {{data.childOrgCount}})</span>
            </div>
          </div>
        </el-tree>
      </el-aside>
      <el-main v-loading="loading">
        <div>
          <el-row>当前选择组织/岗位：</el-row>
          <el-row>
            <el-form class="bgwh radius pt15 pl20 mt-20" inline size="small">
              <el-row>
                <el-form-item label="当前选择组织：" label-width="180px">
                  <span class="dib w150">{{OrganizationData.orgName}}</span>
                </el-form-item>
                <el-form-item label="组织层级：" label-width="180px">
                  <span class="dib w100">{{OrganizationData.orgGrade}}</span>
                </el-form-item>
                <el-form-item label="组织单元代码：" label-width="180px">
                  <span class="dib w100">{{OrganizationData.zCode}}</span>
                </el-form-item>
              </el-row>
              <el-row>
                <el-form-item label="编制情况：" label-width="180px">
                  <span v-show="OrganizationData.isHasOrganization===false">无编制</span>
                  <span v-show="OrganizationData.isHasOrganization===true">存在编制</span>
                  <el-button v-if="showOrgEdit" @click="handleEdit(row)" plain type="primary">编辑</el-button>
                </el-form-item>
              </el-row>
              <el-row v-show="OrganizationData.isHasOrganization===true">
                <el-form-item label="编制类型：" label-width="180px">
                  <span v-show="OrganizationData.organizationType===0">编制到组织</span>
                  <span v-show="OrganizationData.organizationType===10">编制到岗位</span>
                </el-form-item>
                <el-form-item label="编制数量 ：" label-width="180px">
                  <span class="dib w100">{{OrganizationData.organizationNumber}}</span>
                </el-form-item>
              </el-row>
            </el-form>
          </el-row>
        </div>
        <el-table v-if="showPositionList" :data="tableData" class="p15" stripe style="width: 100%">
          <el-table-column label="岗位信息" prop="positionName"></el-table-column>
          <el-table-column label="对应部门" prop="orgName"></el-table-column>
          <el-table-column label="岗位ID" prop="positionCode"></el-table-column>
          <el-table-column label="是否负责岗位" prop="isCharge">
            <template slot-scope="scope">
              <span class="el-icon-check" v-show="scope.row.isCharge===true"></span>
            </template>
          </el-table-column>
          <el-table-column label="岗位编制" prop="organizationNumber">
            <template slot-scope="scope">
              <span v-show="scope.row.organizationNumber===0">-</span>
              <span v-show="scope.row.organizationNumber!==0">{{scope.row.organizationNumber}}</span>
            </template>
          </el-table-column>
          <el-table-column label="备注" prop="organizationRemark"></el-table-column>
          <el-table-column label="操作" width="180">
            <template slot-scope="{ row, $index}">
              <el-row v-show="OrganizationData.isHasOrganization===true && showPositionEdit">
                <el-button @click="handleEditPosition($index, row)" size="small" type="info">修改</el-button>
              </el-row>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>
    <!--组织编制调整-->
    <el-dialog
      :close-on-click-modal="false"
      :visible.sync="editFormVisible"
      style="width: 65%; left: 17.5%"
      title="组织编制调整"
    >
      <el-dialog :visible.sync="innerVisible" append-to-body title="提示" width="30%">
        <div style="text-align: center">
          <p>将要进行操作 组织： 数据</p>
          <p>进行操作内容： 增加组织编制</p>
          <p>
            <br/>
          </p>
          <p>此操作将影响以下存在编制组织，望知悉</p>
          <p style="color: red">{{ChildOrgData}}</p>
          <p>
            <br/>
          </p>
          <p>是否进行操作</p>
          <el-button @click="isHasOrganizationTrue" type="primary">确认</el-button>
          <el-button @click="isHasOrganizationFalse" type="info">取消</el-button>
        </div>
      </el-dialog>
      <el-form :model="editForm" label-width="120px" ref="editForm">
        <el-form-item label="组织：">
          <span class="dib w100">{{OrganizationData.orgName}}</span>
        </el-form-item>
        <el-form-item label="组织单元代码：">
          <span class="dib w100">01040602</span>
        </el-form-item>
        <el-form-item label="编制情况：">
          <el-select
            @change="promptBox"
            clearable
            filterable
            v-model="OrganizationData.isHasOrganization"
          >
            <el-option
              :key="item.val"
              :label="item.name"
              :value="item.val"
              v-for="item of isHasOrganizationList"
            ></el-option>
          </el-select>
        </el-form-item>
        <template>
          <el-form-item label="编制类型：" v-show="OrganizationData.isHasOrganization===true">
            <el-select clearable filterable v-model="OrganizationData.organizationType">
              <el-option
                :key="item.val"
                :label="item.name"
                :value="item.val"
                v-for="item of organizationType"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="组织编制数量：" prop="organizationNumber"
                        v-show="OrganizationData.isHasOrganization===true
&& OrganizationData.organizationType===0">
            <el-input placeholder="请输入" v-model.trim="OrganizationData.organizationNumber"></el-input>
          </el-form-item>
        </template>
        <el-form-item label="备注" prop="organizationRemark">
          <el-input
            :rows="4"
            placeholder="请输入"
            type="textarea"
            v-model.trim="OrganizationData.organizationRemark"
          ></el-input>
        </el-form-item>
      </el-form>
      <div class="dialog-footer" slot="footer">
        <el-button @click.native="editSubmit" type="primary">提交</el-button>
        <el-button @click.native="editFormVisible = false">取消</el-button>
      </div>
    </el-dialog>
    <!--岗位编制修改-->
    <el-dialog
      :close-on-click-modal="false"
      :visible.sync="editPositionVisible"
      style="width: 65%; left: 17.5%"
      title="岗位编制修改"
    >
      <el-form :model="editPositionForm" label-width="120px" ref="editPositionForm">
        <el-form-item label="组织：" prop="orgName">
          <span class="dib w100">{{editPositionForm.orgName}}</span>
        </el-form-item>
        <el-form-item label="岗位：" prop="positionName">
          <span class="dib w100">{{editPositionForm.positionName}}</span>
        </el-form-item>
        <el-form-item label="岗位编号：" prop="positionCode">
          <span class="dib w100">{{editPositionForm.positionCode}}</span>
        </el-form-item>
        <el-form-item label="岗位编制：" prop="organizationNumber">
          <el-input
            auto-complete="off"
            placeholder="请输入"
            v-model.trim="editPositionForm.organizationNumber"
          ></el-input>
        </el-form-item>
        <el-form-item label="备注" prop="organizationRemark">
          <el-input
            :rows="4"
            placeholder="请输入"
            type="textarea"
            v-model.trim="editPositionForm.organizationRemark"
          ></el-input>
        </el-form-item>
      </el-form>
      <div class="dialog-footer" slot="footer">
        <el-button :loading="editLoading" @click.native="editPositionSubmit" type="primary">提交</el-button>
        <el-button @click.native="editPositionVisible = false">取消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  import _ from 'lodash';

  export default {
    data() {
      return {
        value: '',
        searchOrgKey: '',
        treeLoading: true,
        tableData: [], // 列表
        OrganizationData: [], // 顶部信息
        ChildOrgData: '', // 获取下级组织列表
        innerVisible: false, // 内层
        editFormVisible: false,
        loading: false,
        editLoading: false,
        editPositionVisible: false,
        editForm: {},
        editPositionForm: {},
        // 表单属性,绑定到模态框的v-model
        form: {
          prepareStatus: undefined,
        },
        isHasOrganizationList: [
          // 编制情况
          {val: false, name: '不存在编制'},
          {val: true, name: '存在编制'},
        ],
        organizationType: [
          // 编制类型
          {val: 0, name: '编制到组织'},
          {val: 10, name: '编制到岗位'},
        ],
        treeProps: {
          label: 'label',
          children: 'children',
          isLeaf: (data) => !data.isOrg,
          childOrgCount: 0,
          positionCount: 0,
          isOrg: false,
          organizationType: '',
          isHasOrganization: false,
        },
        search: {
          userName: '',
          positionName: '',
          parentOrgId: 0,
        },
        orgName: '',
        treeObj: {
          node: undefined,
          resolve: undefined,
        },
      };
    },
    computed: {
      action() {
        return this.$store.state.user.action;
      },
      showOrgEdit() {
        return !!this.action['md.action.hr.authcount.org.edit'];
      },
      showPositionList() {
        return !!this.action['md.action.hr.authcount.position.list'];
      },
      showPositionEdit() {
        return !!this.action['md.action.hr.authcount.position.edit'];
      },
    },
    methods: {
      // eslint-disable-next-line func-names
      getRemoteFollow: _.debounce(function () {
        this.searchOrgHander();
      }, 1),
      searchOrgHander() {
        this.treeObj.node.childNodes = [];
        if (this.searchOrgKey.length === 0) {
          this.loadNode(this.treeObj.node, this.treeObj.resolve);
        } else {
          this.searchNode(this.treeObj.node, this.treeObj.resolve);
        }
      },
      async searchNode(node, resolve) {
        const orgData = await this.$http.get(`/mdApi/api/Org/GetOrganizationListByName?orgName=${this.searchOrgKey}`);
        const treeData = [];
        orgData.data.forEach((element) => {
          treeData.push({
            id: element.id,
            label: element.orgName,
            childOrgCount: element.organizationNumber,
            positionCount: element.childOrganizationNumber,
            isOrg: true,
            organizationType: element.organizationType,
            isHasOrganization: element.isHasOrganization,
          });
        });
        resolve(treeData);
      },
      // 点击树
      handleNodeClick(data) {
        const {id, label, isOrg} = data;
        if (isOrg) {
          this.orgName = label;
          this.search.parentOrgId = id;
          this.getOrganization(id);
        }
      },
      /**
       *通过组织Id获取岗位信息
       * * */
      getOrganization(currentId) {
        Promise.all([
          this.$http.get(`/mdApi/api/Org/GetOrganization/${currentId}`),
          this.$http.get(`/mdApi/api/Position/GetPositionOrganizationByOrgId/${currentId}`),
        ]).then(([{data: OrganizationData}, {data: positionData}]) => {
          this.OrganizationData = OrganizationData;
          this.tableData = positionData;
        });
      },
      /**
       * 懒加载树获取组织机构子节点
       * element-tree使用方法
       * @param node:当前点击节点信息
       * @param resolve:传递参数方法
       * */
      loadNode(node, resolve) {
        this.treeObj.node = node;
        this.treeObj.resolve = resolve;
        const currentId = node.level === 0 ? 0 : node.data.id;
        const treeData = [];
        Promise.all([
          this.$http.get(`/mdApi/api/Org/GetOrganizationTree/${currentId}`),
          this.$http.get(`/mdApi/api/Position/GetPositionOrganizationByOrgId/${currentId}`),
        ]).then(([{data: orgData}, {data: positionData}]) => {
          orgData.forEach((element) => {
            treeData.push({
              id: element.id,
              label: element.orgName,
              childOrgCount: element.childOrganizationNumber,
              positionCount: element.organizationNumber,
              isOrg: true,
              organizationType: element.organizationType,
              isHasOrganization: element.isHasOrganization,
            });
          });
          this.tableData = positionData;
          positionData.forEach((element) => {
            treeData.push({
              children: [],
              id: element.id,
              label: element.positionName,
              isLeaf: true,
              isOrg: false,
              isManager: true,
            });
          });
          resolve(treeData);
          if (currentId === 0) this.treeLoading = false;
        });
      },
      /**
       *显示编辑页面
       * */
      handleEdit(row) {
        // this.getCaseGroup();
        this.editFormVisible = true;
        this.editForm = Object.assign({}, row);
      },
      /**
       *显示岗位修改页面
       * */
      handleEditPosition(index, row) {
        // this.getCaseGroup();
        this.editPositionVisible = true;
        this.editPositionForm = Object.assign({}, row);
      },
      /**
       *编辑组织编制调整
       * */
      async editSubmit() {
        this.loading = true;
        try {
          const params = {
            id: Number(this.OrganizationData.id),
            isHasOrganization: this.OrganizationData.isHasOrganization,
            organizationNumber: this.OrganizationData.organizationNumber,
            organizationType: this.OrganizationData.organizationType,
            organizationRemark: this.OrganizationData.organizationRemark,
          };
          // const params = await this.$refs.formRef.validate();
          const {message} = await this.$http.put(
            `/mdApi/api/Org/EditOrgOrganization/${this.OrganizationData.id}`,
            params,
          );
          this.$message.success(message);
          this.loading = false;
          this.editFormVisible = false;
        } catch (error) {
          this.$message.error(error.message);
        }
      },
      /**
       *岗位编制修改
       * */
      async editPositionSubmit() {
        this.loading = true;
        try {
          const params = {
            id: Number(this.editPositionForm.id),
            organizationNumber: Number(this.editPositionForm.organizationNumber),
            organizationRemark: this.editPositionForm.organizationRemark,
          };
          const {message} = await this.$http.put(
            `/mdApi/api/Position/EditPositionOrganization/${this.editPositionForm.id}`,
            params,
          );
          this.$message.success(message);
          this.loading = false;
          this.editPositionVisible = false;
          this.getOrganization(this.OrganizationData.id);
          // this.loadNode(this.treeObj.node, this.treeObj.resolve);
        } catch (error) {
          this.$message.error(error.message);
        }
      },
      /**
       *从无编制切换到有编制得提示框
       * */
      async promptBox() {
        await this.GetChildOrgById();
        if (this.OrganizationData.isHasOrganization === true && this.ChildOrgData.length !== 0) {
          this.innerVisible = true;
        }
      },
      /**
       *获取下级组织列表
       * */
      GetChildOrgById() {
        return Promise.all([this.$http.get(`/mdApi/api/Org/GetChildOrgById?OrgId=${this.OrganizationData.id}`)]).then(
          ([{data: childOrgData}]) => {
            console.log(1000);
            this.ChildOrgData = childOrgData.reduce((str, item) => `${str + item.orgName}、`, '');
            console.log(this.ChildOrgData);
          },
        );
      },
      /**
       *弹框取消、确定操作
       */
      isHasOrganizationTrue() {
        this.innerVisible = false;
      },
      isHasOrganizationFalse() {
        this.innerVisible = false;
        this.OrganizationData.isHasOrganization = false;
      },
    },
  };
</script>

<style scoped>
  .p15 {
    padding: 15px;
  }

  .manager {
    color: #44c788;
  }

  .el-form-item label:after {
    content: '';
    display: inline-block;
    width: 100%;
  }

  .el-form-item__label {
    text-align: justify;
    height: 50px;
  }

  .el-form-item.is-required .el-form-item__label:before {
    content: none !important;
  }
</style>
