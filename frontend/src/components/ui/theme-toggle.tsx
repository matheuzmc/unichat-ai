import * as React from "react"
import { FaMoon, FaSun } from "react-icons/fa"

import { Button } from "@/components/ui/button"

export function ThemeToggle() {
  const [theme, setThemeState] = React.useState<"light" | "dark">("light")

  React.useEffect(() => {
    const isDarkMode = document.documentElement.classList.contains("dark")
    setThemeState(isDarkMode ? "dark" : "light")
  }, [])

  function toggleTheme() {
    const newTheme = theme === "light" ? "dark" : "light"
    setThemeState(newTheme)
    
    if (newTheme === "dark") {
      document.documentElement.classList.add("dark")
    } else {
      document.documentElement.classList.remove("dark")
    }
  }

  return (
    <Button
      variant="outline"
      size="icon"
      onClick={toggleTheme}
      className="border border-border rounded-full bg-background"
    >
      {theme === "light" ? (
        <FaSun className="h-[1.2rem] w-[1.2rem] text-amber-500" />
      ) : (
        <FaMoon className="h-[1.2rem] w-[1.2rem] text-indigo-400" />
      )}
      <span className="sr-only">
        {theme === "light" ? "Alternar para modo escuro" : "Alternar para modo claro"}
      </span>
    </Button>
  )
} 