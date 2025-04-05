import React from 'react'
import ChatWindow from './components/ChatWindow'
import { ThemeToggle } from './components/ui/theme-toggle'

function App() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-background to-background/90 p-4">
      <header className="w-full max-w-4xl mb-6 text-center flex flex-col items-center">
        <h1 className="text-3xl font-bold mb-2 text-foreground">UniChat</h1>
        <p className="text-lg text-muted-foreground max-w-md">
          Seu assistente acadêmico inteligente.
        </p>
      </header>
      
      <main className="w-full max-w-4xl h-[600px] relative">
        <div className="absolute right-4 -top-14 z-10">
          <ThemeToggle />
        </div>
        <ChatWindow />
      </main>
      
      <footer className="mt-6 text-sm text-muted-foreground">
        &copy; {new Date().getFullYear()} UniChat - Todos os direitos reservados
      </footer>
    </div>
  )
}

export default App
