module.exports = {
  app: {
    host: '0.0.0.0', // host
    port: '8001', // port
    apiPrefix: '/api/v1' // api 前缀
  },
  db: {
  //  url: 'mongodb://otcgo.cn:u3fhhrPr@114.215.30.71:27017,114.215.30.71:27018,114.215.30.71:27019/neo-otcgo?replicaSet=rs0',
   // url: 'mongodb://114.215.30.71:27020/neo-otcgo',
    url: 'mongodb://114.215.30.71:27017/neo-otcgo?replicaSet=rs1',
   // otcgo.cn:u3fhhrPr
   // url: 'mongodb://114.215.30.71:27017/neo-otcgo?replicaSet=rs0',
  //  url: 'mongodb://otcgo:u3fhhrPr@127.0.0.1:27020/neo-otcgo?replicaSet=rs0',
   //
    options: {
      useMongoClient: true,
      user: 'otcgo',
      pass: 'u3fhhrPr',
      auth: {
        authdb: 'admin'
      }
    },
    debug: true
  },
  rpc: 'http://seed2.neo.org:10332',
  log: {
    appenders: [ // 日志
      {
        type: 'console'
      }, // 控制台输出
      {
        type: 'file',
        filename: 'logs/http.log',
        maxLogSize: 20480,
        backups: 1,
        category: 'http',
        layout: {
          type: 'json',
          separator: ','
        }
      },
      {
        type: 'file',
        filename: 'logs/db.log',
        maxLogSize: 52428800,
        backups: 2,
        category: 'db',
        layout: {
          type: 'json',
          separator: ','
        }
      },
      {
        type: 'file',
        filename: 'logs/init.log',
        maxLogSize: 20480,
        backups: 1,
        category: 'init',
        layout: {
          type: 'json',
          separator: ','
        }
      },
      {
        type: 'file',
        filename: 'logs/nep5.log',
        maxLogSize: 52428800,
        backups: 2,
        category: 'nep5',
        layout: {
          type: 'json',
          separator: ','
        }
      }
    ]
  }
}
