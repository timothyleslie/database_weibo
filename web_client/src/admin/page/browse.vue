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
                <el-table-column label="点赞数" prop="like_cnt" width="70px" ></el-table-column>
                <el-table-column label="转发数" prop="transmit_cnt" width="70px" ></el-table-column>
                <el-table-column label="评论数" prop="comment_cnt" width="70px" ></el-table-column>
                <el-table-column>
                    <template slot-scope="scope" width="100px">
                        <el-button type="text" @click="like(scope.row)" >点赞</el-button>
                        <el-button type="text" @click="favorite(scope.row)" >收藏</el-button>
                        <el-button type="text" @click="transmit(scope.row)" >转发</el-button>
                        <el-button type="text" @click="comment(scope.row)" >评论</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <el-dialog
            width="30%"
            title="添加微博"
            :visible.sync="dialogFormVisibleed1">
            <div class="form-box">
                <el-form :model="form" :rules="rules" ref="form" label-width="150px">
                    <el-form-item label="内容" prop="content">
                        <el-input v-model="form.content" placeholder="请输入微博内容"></el-input>
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
        if(localStorage.getItem('username')===""){
            this.$router.replace('/login')
        }else{this.init();}
    },
    methods:{
        init(){
            this.$http.post(main.url+"/article/list",
                {'uid': 0},
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
        submit(form){ //修改收藏内容，提交
            this.$http.post(main.url+"/favorite/update",
                {
                    'id': this.form.id,
                    'wname': this.form.wname,
                    'wurl': this.form.wurl,
                    'type': this.form.type
                },
                {
                    headers: {'Content-Type':'application/x-www-form-urlencoded'},
                    emulateJSON: true
                }).then(
                success=> {
                    this.$message({type: 'success', message: '修改成功'});
                    this.form={
                        id: '',
                        wname:'',
                        wurl:'',
                        type:''
                    };
                    this.dialogFormVisibleed = false;
                    this.init();
                }
            )
        },
        addfavorite(){this.dialogFormVisibleed1=true},
        addnew(form){ //添加新收藏
            // if(this.form.wname==="")
            //     this.$message({type: 'error', message: '网站名称！'});
            if(this.form.content==="")
                this.$message({type: 'error', message: '微博内容不能为空！'});
                // else if(this.form.type==="")
            //     this.$message({type: 'error', message: '请设置权限！'});
            else{
                this.$http.post(main.url+"/article/add",
                    {
                        'uid': localStorage.getItem('id'),
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
        },
        comment(row)
        {
            localStorage.setItem('article_id', row.id);
            this.$router.push({ path: '/comment' })
        }
    }
}
</script>
