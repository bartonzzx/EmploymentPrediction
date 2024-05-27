interface db_config {
  db_name: string
  db_addr: string
  db_user: string
  db_pwd: string
  db_score: string
  db_course: string
  db_ability: string
  db_prediction: string
  db_statistics: string
  db_student: string
}

const config: db_config = {
  db_name: 'employmentprediction',
  db_addr: 'localhost',
  db_user: 'root',
  db_pwd: '123456',
  db_score: 'test_score',
  db_course: 'test_course',
  db_ability: 'test_ability',
  db_prediction: 'test_possibility_record',
  db_statistics: 'test_statistics',
  db_student: 'test_student',
}

export default config
