/**
 * Filename: /Users/wei/Desktop/otcgo/neo_scrapy/src/modules/rpx/rpx.ts
 * Path: /Users/wei/Desktop/otcgo/neo_scrapy
 * Created Date: Thursday, November 16th 2017, 12:14:47 am
 * Author: wei
 *
 * Copyright (c) 2017 Your Company
 */

import * as log4js from 'log4js'
import * as config from 'config'
import { Router } from 'express'
import { NRequest } from '../../interface'
import * as graphqlHTTP from 'express-graphql'
import * as neon from '@cityofzion/neon-js'
import { Request as WebHandler } from '../../utils'
import schema from '../../graphql'


const logger = log4js.getLogger('nep5')
const nep5: Router = Router()

nep5.use(`/public/graphql`, graphqlHTTP({
  schema,
  graphiql: true,
  pretty: true,
  extensions ({
    documet,
    variables,
    operationName,
    result
  }) {
    if (result.errors) {
      result.error_code = 500
      result.error_msg = result.errors[0].message
      delete result.errors
      result.status = 'Error'
    } else {
      result.code = 200
      result.status = 'OK'
      result.server_time = new Date()
    }
  }
}))


nep5.get(`/address/balanceOf`,  async (req: NRequest, res: any)  => {
    try {
      logger.info(`${config.get('rpc')}`)
      const result: any = await WebHandler({
        url: `${config.get('rpc')}`,
        method: 'post',
        json: {
          jsonrpc: '2.0',
          method: 'invokefunction',
          params: [
            'ecc6b20d3ccac1ee9ef109af5a7cdb85706b1df9',
            'balanceOf',
            [
              {
                type: 'Hash160',
                value: 'bfc469dd56932409677278f6b7422f3e1f34481d'
              }
            ]
          ],
          id: 3
        }
      })
      console.log('0x' + result.result.stack[0].value.toString(10).toString(10))
     console.log(neon.u.fixed82num(result.result.stack[0].value))
     return res.apiSuccess('11')
    } catch (error) {
      logger.error('nep5', error)
      return res.apiError(error)
    }
  })

export { nep5 }



