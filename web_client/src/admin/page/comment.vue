<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-setting"></i> 管理</el-breadcrumb-item>
                <el-breadcrumb-item>收藏列表</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div>
            <el-table :data="data" border style="width: 90%" ref="multipleTable" >
                <el-table-column label="ID" prop="id" width="80px" ></el-table-column>
                <el-table-column label="作者" prop="wname" width="100px" ></el-table-column>
                <el-table-column label="内容" prop="content" width="300px" ></el-table-column>
                <el-table-column label="发表时间" prop="ctime" width="250px" ></el-table-column>
            </el-table>
            <el-button type="primary" @click="addcomment()" align="center">添加新评论</el-button>
        </div>
        <el-dialog
            width="30%"
            title="添加微博"
            :visible.sync="dialogFormVisibleed1">
            <div class="form-box">
                <el-form :model="form" :rules="rules" ref="form" label-width="150px">
                    <el-form-item label="内容" prop="content">
                        <el-input v-model="form.content" placeholder="请输入评论内容"></el-input>
                    </el-form-item>
                    <el-form-item style="text-align: center" >
                        <el-button @click="dialogFormVisibleed1 = false" >取消</el-button>
                        <el-button type="primary" @click="addnew(form)">添加</el-button>
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
        if(localStorage.getItem('article_id')===""){
            this.$router.replace('/admin/browse')
        }else{this.init();}
    },
    methods:{
        init(){
            this.$http.post(main.url+"/article/comment",
                {'aid': localStorage.getItem('article_id')},
                {
                    headers: {'Content-Type':'application/x-www-form-urlencoded'},
                    emulateJSON: true
                }).then(
                success=>{
                    this.data=success.data;
                    // for(let i=0;i<this.data.length;i++){
                    //     if(this.data[i].type===0)
                    //         this.data[i].type = "公开";
                    //     else
                    //         this.data[i].type = "私有";
                    // }
                }
            );
        },
        addcomment(){this.dialogFormVisibleed1=true},
        addnew(form){ //添加新评论
            // if(this.form.wname==="")
            //     this.$message({type: 'error', message: '网站名称！'});
            if(this.form.content==="")
                this.$message({type: 'error', message: '评论内容不能为空！'});
            else{
                this.$http.post(main.url+"/comment/add",
                    {
                        'uid': localStorage.getItem('id'),
                        'aid': localStorage.getItem('article_id'),
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
        like(row){ //点赞
            this.$http.post(main.url+"/article/like",
                {  'uid': localStorage.getItem('id'),
                    'aid': row.id,},
                {
                    headers: {'Content-Type':'application/x-www-form-urlencoded'},
                    emulateJSON: true
                }).then(
                success=> {
                    this.$message({type: 'success', message: '已点赞'});
                    this.init();
                }
            );
        },
        favorite(row){
            this.$http.post(main.url+"/article/favorite",
                {  'uid': localStorage.getItem('id'),
                    'aid': row.id,},
                {
                    headers: {'Content-Type':'application/x-www-form-urlencoded'},
                    emulateJSON: true
                }).then(
                success=> {
                    this.$message({type: 'success', message: '已收藏'});
                    this.init();
                }
            );
        },
        transmit(row){
            this.$http.post(main.url+"/article/transmit",
                {  'uid': localStorage.getItem('id'),
                    'aid': row.id,},
                {
                    headers: {'Content-Type':'application/x-www-form-urlencoded'},
                    emulateJSON: true
                }).then(
                success=> {
                    this.$message({type: 'success', message: '已收藏'});
                    this.init();
                }
            );
        }
    }
}
</script>

<style scoped>
.tab{
    position: absolute;
    top: 20%;
    left: 25%;
    width: 805px;
    height: 100%;
}
.login-wrap{
    position: relative;
    background: url("/static/img/bg.jpg") no-repeat center;
    width:100%;
    height:100%;
}
.ms-title{
    position: absolute;
    top: 40%;
    width: 100%;
    margin-top: -230px;
    text-align: center;
    font-size: 14px;
    color: #fff;
    font-weight: bold;
}
.login-btn button{
    position: absolute;
    width: 40%;
    height: 35px;
    right: 10%;
    top: 10%;
}
</style>
