import process from 'node:process'
import fastify from 'fastify'
import type { MySQLPromisePool } from '@fastify/mysql'
import fastifymysql from '@fastify/mysql'
import fastifyCors from '@fastify/cors'

// pass promise = true
declare module 'fastify' {
  interface FastifyInstance {
    mysql: MySQLPromisePool
  }
}

// 创建 Fastify 实例
const server = fastify({ logger: true })
server.register(fastifymysql, {
  promise: true,
  connectionString: 'mysql://root:123456@localhost:3306/employmentprediction',
})

server.register(fastifyCors, {
  origin: '*', // 允许所有来源
  methods: ['GET', 'POST'], // 允许的请求方法
})

// 注册路由
// user/login 用户登录

// user/permission 获取用户权限

// user/password/edit 修改用户密码

// app/route/list 后端获取路由数据

// app/menu/list 基于文件系统路由模式下，后端获取导航菜单数据

// score_management/score 获取个人成绩
server.get('/score_management/score', async (request, reply) => {
  const db: MySQLPromisePool = server.mysql
  try {
    const [rows] = await db.query('SELECT coursename,(case when natureofexam = 1 then "正常考试" when natureofexam = 0.8 then "重考重修" end) as natureofexam,credit,score FROM test_score where stu_id="2014550620"')
    reply.send(rows)
  }
  catch (err) {
    reply.send(err)
  }
})

// course_management/course 获取课程与能力对应矩阵
server.get('/course_management/course', async (request, reply) => {
  const db: MySQLPromisePool = server.mysql
  try {
    const [rows] = await db.query('select * from test_course')
    reply.send(rows)
  }
  catch (err) {
    reply.send(err)
  }
})

// 分页查询，暂留
// server.get('/course_management/course', async (request, reply) => {
//   const db: MySQLPromisePool = server.mysql

//   // 获取分页参数，默认值 page=1, limit=10
//   const { page = 1, limit = 10 } = request.query as { page?: number, limit?: number }
//   const offset = (page - 1) * limit

//   try {
//     // 执行分页查询
//     const [rows] = await db.query('SELECT * FROM test_course LIMIT ? OFFSET ?', [limit, offset])

//     // 获取总数
//     const [countResult] = await db.query('SELECT COUNT(*) AS total FROM test_course')
//     const total = (countResult as any)[0].total

//     // 返回分页结果
//     reply.send({
//       data: rows,
//       pagination: {
//         total,
//         page,
//         limit,
//         totalPages: Math.ceil(total / limit),
//       },
//     })
//   } catch (err) {
//     reply.send(err)
//   }
// })

// employment_management/ability_evaluation/personal_ability 获取个人能力数据
// server.post('/employment_management/ability_evaluation/personal_ability')

// employment_management/ability_evaluation/yearly_ability 获取年级能力数据

// employment_management/employment_prediction/employment 获取个人就业去向预测数据

// employment_management/realtime_evaluation_prediction/realtime 实时评估个人能力数据

// employment_management/realtime_evaluation_prediction/realtime 实时预测个人就业去向

// 启动服务器
async function start() {
  try {
    await server.listen(3000, '0.0.0.0')
    server.log.info(`Server is running at http://localhost:3000`)
  }
  catch (err) {
    server.log.error(err)
    process.exit(1)
  }
}

start()
