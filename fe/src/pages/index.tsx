import { useRouter } from 'next/router'
import { useEffect } from "react";

export default function main() {
  const router = useRouter()
  useEffect(() => {
    router.push('/login')
  })
  return (null)
}
