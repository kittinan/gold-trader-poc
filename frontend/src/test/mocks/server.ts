import { setupServer } from 'msw/node'
import { handlers } from './handlers'

// MSW server setup
export const server = setupServer(...handlers)

// Setup and teardown utilities
export const setupMSW = () => {
  server.listen({
    onUnhandledRequest: 'warn',
  })
}

export const teardownMSW = () => {
  server.close()
}

export const resetHandlers = () => {
  server.resetHandlers()
}
