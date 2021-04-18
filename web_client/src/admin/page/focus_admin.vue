<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-setting"></i> 浏览</el-breadcrumb-item>
                <el-breadcrumb-item>所有用户</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div>
            <el-table :data="data" border style="width: 90%" ref="multipleTable" >
                <el-table-column label="用户ID" prop="id" width="80px" ></el-table-column>
                <el-table-column label="用户名" prop="wname" width="100px" ></el-table-column>
                <el-table-column>
                    <template slot-scope="scope" width="100px">
                        <el-button type="text" @click="follow(scope.row)" >关注</el-button>
                        <el-button type="text" @click="private_msg(scope.row)" >私信</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <el-dialog
            width="30%"
            title="私信"
            :visible.sync="dialogFormVisibleed1">
            <div class="form-box">
                <el-form :model="form" :rules="rules" ref="form" label-width="150px">
                    <el-form-item label="内容" prop="content">
                        <el-input v-model="form.content" placeholder="请输入私信内容"></el-input>
                    </el-form-item>
                    <el-form-item style="text-align: center" >
                        <el-button @click="dialogFormVisibleed1 = false" >取消</el-button>
                        <el-button type="primary" @click="addnew(form)">发送</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </el-dialog>
    </div>
</template>

<script>
import main from "../../main";

export default {
    data: function(){
        return {
            data:[],
            options:[{value: 0, label: "公开"},{value: 1, label: "私有"}],
            dialogFormVisibleed:false,
            dialogFormVisibleed1:false,
            form:{
                id: '',
                wname:'',
                content:'',
                type:''
            },
            rules:{
                wname:[
                    {required:true,message:'请输入网站名称',trigger:'blur'}
                ],
                wurl:[
                    {required:true,message:'请输入网站地址',trigger:'blur'}
                ],
                type:[
                    {required:true,message:'请设置权限',trigger:'blur'}
                ]
            }
        }
    },
    created(){
        if(localStorage.getItem('username')===""){
            this.$router.replace('/login')
        }else{this.init();}
    },
    methods:{
        init(){
            this.$http.post(main.url+"/user/list",
                {'uid': localStorage.getItem('id')},
                {
                    headers: {'Content-Type':'application/x-www-form-urlencoded'},
                    emulateJSON: true
                }).then(
                success=>{
                    this.data=success.data;
                }
            );
        },
        private_msg(row){localStorage.setItem('receiver', row.id);
                        this.dialogFormVisibleed1=true;},
        addnew(form){ //添加新私信
            // if(this.form.wname==="")
            //     this.$message({type: 'error', message: '网站名称！'});
            if(this.form.content==="")
                this.$message({type: 'error', message: '微博内容不能为空！'});
                // else if(this.form.type==="")
            //     this.$message({type: 'error', message: '请设置权限！'});
            else{
                this.$http.post(main.url+"/private_msg/add",
                    {
                        'uid': localStorage.getItem('id'),
                        'receiver_id': localStorage.getItem('receiver'),
                        'content': this.form.content,
                    },
                    {
                        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                        emulateJSON: true
                    }).then(
                    success => {
                        this.$message({type: 'success', message: '添加成功'});
                        this.form = {
                            id: '',
                            wname:'',
                            wurl:'',
                            type:''
                        };
                        this.init();
                    }
                );
                this.dialogFormVisibleed1 = false;
            }
        },
        follow(row){ //关注
            this.$http.post(main.url+"/follow/add",
                {  'uid': localStorage.getItem('id'),
                    'follow_id': row.id,},
                {
                    headers: {'Content-Type':'application/x-www-form-urlencoded'},
                    emulateJSON: true
                }).then(
                success=> {
                    this.$message({type: 'success', message: '已关注'});
                    this.init();
                }
            );
        }
    }
}
</script>
