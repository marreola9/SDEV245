import { serve } from '@hono/node-server'
import { Hono } from 'hono'
import { basicAuth } from 'hono/basic-auth'
import { logger } from 'hono/logger'
const app = new Hono()

app.get('/', (c) => {
  return c.text('Hello Hono!')
})
app.use('*', logger())
app.use('/admin/*', basicAuth({username: 'carmen', password: '1234'}))
app.use('/users/*', basicAuth({username: 'carmen', password: '4321'}))

app.get('/admin', (c) => {
  return c.text('This is the admin dashboard.')
})

app.get('/users', (c) => {
  return c.text('This is the users dashboard.')
})


serve({
  fetch: app.fetch,
  port: 3000
}, (info) => {
  console.log(`Server is running on http://localhost:${info.port}`)
})

// The part of the CIA tirad that focuses on is availability 
// using a password to authentication the correct user