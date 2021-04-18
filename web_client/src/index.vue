<template>
    <div class="login-wrap">
        <div class="ms-title" style="font-size: 30px">全部微博<span style="font-size: 10px; margin-left: 73px;">
            <u></u></span>
        </div>
        <div class="tab">
            <el-table :data="data" border ref="multipleTable" >
                <el-table-column label="文章ID" prop="id" width="80px" ></el-table-column>
                <el-table-column label="作者" prop="wname" width="100px" ></el-table-column>
                <el-table-column label="内容" prop="content" width="300px" ></el-table-column>
                <el-table-column label="发表时间" prop="ctime" width="250px" ></el-table-column>
                <el-table-column label="点赞数" prop="like_cnt" width="70px" ></el-table-column>
                <el-table-column label="收藏数" prop="favorite_cnt" width="70px" ></el-table-column>
                <el-table-column label="评论数" prop="comment_cnt" width="70px" ></el-table-column>
            </el-table>
        </div>
        <el-button type="primary" @click="submit()" >登录</el-button>
        <el-button type="primary" @click="register()" >注册</el-button>

    </div>
</template>

<script>
    import main from './main';
    export default {
        data: function(){
            return {
                dialogVisible:false,
                data:[]
            }
        },
        created(){
            this.init();
        },
        methods: {
            init(){
                this.$http.post(main.url+"/article/list",
                    {'uid': 0},
                    {
                        headers: {'Content-Type':'application/x-www-form-urlencoded'},
                        emulateJSON: true
                    }).then(
                    success=>{
                        this.data=success.data;
                    }
                );
            },
            gotourl(row){ //进入指定的网站
                this.$http.post(main.url+"/favorite/count",
                    {'id': row.id},
                    {
                        headers: {'Content-Type':'application/x-www-form-urlencoded'},
                        emulateJSON: true
                    }).then(
                    success=> {
                        window.open(row.wurl, "_blank");
                        this.init();
                    }
                )
            },
            submit(){
                this.$router.push({ path: '/login' });
            },
            register(){
                this.$router.push({ path: '/register' });
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
