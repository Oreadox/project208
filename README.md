# project208
# 接口文档
#### 除了登陆授权获取基本信息其他路由带上请求头
Authorization: Bearer
###
## 登录
#### URL /api/user/login
### POST
```
{
    "username":"5907118053"  //学号
    "password":"123456"  
}
```
#### RETURN
```
{
    "status":1,
    "message":"登录成功",
    "token":"dasdadasdadadadad",
    "name": "郭昕宇",
    "sex": 1 or 2 //1男2女
}
or
{
    "status":0,
    "message":"密码错误"
}
```

## 获取单个题目
#### URL /api/question?id=ID
### GET
##### request header 
Authorization: Bearer
### return
```
{
    "status":1,
    "message":"获取成功！",
    "data":{
        "id": 1,  //题目id
        'subject': what,  // 题目问题
        'options':["这是选项A"，"这是选项B"，"这是选项C","这是选项D"]    
    }
}
//  id不对返回404
```
## 获取所有题目
### URL /api/question
### GET
##### request header 
Authorization: Bearer
### return
```
{
    "status":1,
    "message":"获取成功",
    "data":[
        {
            "id":1,  //题目的唯一标识符
            "question":"我喜欢吃水果吗",
            "options":[
                "这是A",
                "这是B",
                "这是C",
                "这是D"
            ]
            
        },
        {
            "id":2,  //题目的唯一标识符
            "question":"我喜欢吃饭吗",
            "options":[
                "这是A",
                "这是B",
                "这是C",
                "这是D"
            ]
            
        }，
        {...}
    ]

```



## 获取默认（待选择）的留言
#### URL 
### GET /api/question/message
##### request header 
Authorization: Bearer
### return
```angular2

{
    "status":1,
    "message":"获取成功！",
    "data":{
        "total": 3, // 留言总数
        "content":["留言1","留言2","留言3"] // 列表
        
    }
}
```
## 获取我发布的题目
### GET  /api/question/my
##### request header
Authorization: Bearer
### return
```
{
    "status": 1,
    "message": "成功",
    "data": [
        {
            "set_id": 1,  //题组id
            "questions": {
                "1": "B" , //题目id： 设置的答案
                "2": "A"
            },
            "messages": "出题者设置的留言",
            "all_answers": [
                {
                    "answer_man": "5907118053",  //回答者id
                    "name":"郭昕宇"，
                    "sex":1,
                    "answers": {
                        "1": "B", // 题目id, 回答者的答案
                        "2": "B"
                        
                    },
                    "time": "2019-05-11 13:01:06", //回答时间
                    "score": "20" // 分数
                },
                {
                    "answer_man": "5907118052,
                    "name": "小红",
                    "sex":0,
                    "answers": {
                        "1": "C"
                    },
                    "time": "2019-05-12 03:16:48",
                    "score": "50"
                }
            ]
        },
        {
            "set_id": 4,
            "questions": {
                "1": "A"
            },
            "messages": "",
            "all_answers": [...]
        }
    ]
}
```

 ## 出题
 
 ### URL /api/question/my
 ##### request header
Authorization: Bearer
 ### POST 
 ```
 {
    "questions":{
        "1":"B",
        "2":"C"  //题目id： 出题者设置的答案
        ...
    },
    "messages":"出题者设置的留言"
 }

```
### RETURN
```
{
    "status":1,
    "message":"出题成功"
    "set_id":6
}
```
## 获取我回答的问题
### GET /api/answer/my
##### request header
Authorization: Bearer
### RETURN

```
{
    "status": 1,
    "message": "获取成功",
    "data": [
        {
            "id": 1,  // 回答问题的键
            "user_id": 1,  //出题人id
            "set_id": 1,  // 题组id
            "set_sex": 1 or 2 // 1男2女
            "answers": {
                "1": "B" //答题人的huida
            },
            "messsage": "答题人的留言，如果score超过60就有这一项",
            "create_time": "2019-05-11 13:01:06",
            "score": "80",  
            "real_answer": {
                "1": "A"  //出题人设置的真正答案
            }
        },
        {
            "id": 3,
            "user_id": 2,
            "set_id": 1,
            "answers": {
                "1": "C"
            },
            "messsage": "dsdsads",
            "create_time": "2019-05-12 03:16:48",
            "score": "50",
            "real_answer": {
                "1": "a"
            }
        }
    ]
}

```

## 答题
### URL　/api/answer/my
##### request header
Authorization: Bearer
### POST
``` 
{
    "set_id":"1"  //题组号
    "answer": {
            "1":"B",  //题目序号：回答的答案
            "2":"A",
            ...
            
    },
    "message":"回答问题的人给出题者的留言"
}
```
### RETURN
```
{
    "status":"1",
    "message":"提交成功"，
    "data":{
        "score":60,
        "message":"出题者的留言，分数高于６０就有此列"
    }
    
}

```
## 判断是是否答过题
### URL　/api/answercheck/<int:set_id>
##### request header
Authorization: Bearer
### GET

## RETURN
```


{
    "status":0,
    "message":"你已经回答过题了" "你不能回答自己出的题~"
}
{
    "status":1,
    "message":"没有回答过"

}
```





## 根据set_id获取题组
### URL /api/getset/<int:id>

#### GET

#### return

```

{
    "status": 1,
    "message": "成功！",
    "data": [
        {
            "id": 2,
            "question": "我喜欢去哪里",
            "options": [
                "北京",
                "上海",
                "广州",
                "深圳"
            ]
        },
        {
            "id": 4,
            "question": "我喜欢那种饭",
            "options": [
                "牛肉饭",
                "咖喱饭",
                "煲仔饭",
                "牛逼"
            ]
        },
        {
            "id": 1,
            "question": "我喜欢什么水果",
            "options": [
                "苹果",
                "香蕉",
                "梨",
                "桃子"
            ]
        },
        {
            "id": 3,
            "question": "我喜欢男的女的",
            "options": [
                "男的",
                "女的",
                "中性",
                "人妖"
            ]
        }
    ]
}

```

