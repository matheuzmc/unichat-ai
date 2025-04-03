import React from 'react'
import ChatWindow from './components/ChatWindow'

function App() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <header className="w-full max-w-4xl mb-6 text-center">
        <h1 className="text-3xl font-bold mb-2">UniChat</h1>
        <p className="text-lg text-gray-700">
          Seu assistente acadêmico inteligente.
        </p>
      </header>
      
      <main className="w-full max-w-4xl h-[600px]">
        <ChatWindow />
      </main>
      
      <footer className="mt-6 text-sm text-gray-500">
        &copy; {new Date().getFullYear()} UniChat - Todos os direitos reservados
      </footer>
    </div>
  )
}

export default App
