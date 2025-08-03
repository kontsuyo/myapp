import type { ReactNode } from "react"
import { Box, Container, Flex, Heading, Stack, Spacer } from "@chakra-ui/react"
import { Link as RouterLink } from "react-router-dom"
import { ColorModeButton } from "../ui/color-mode"

interface LayoutProps {
  children: ReactNode
}

const Layout = ({ children }: LayoutProps) => (
  <Box minH="100vh" bg="gray.50" _dark={{ bg: "gray.800" }}>
    <Flex as="header" p={4} align="center" bg="white" _dark={{ bg: "gray.900" }} boxShadow="sm">
      <RouterLink to="/" style={{ textDecoration: "none" }}>
        <Heading size="md">
          🚴‍♂️ Bike Community
        </Heading>
      </RouterLink>
      <Spacer />
      <Stack direction="row" gap={4}>
        <RouterLink to="/posts" style={{ textDecoration: "none" }}>
          投稿一覧
        </RouterLink>
        <RouterLink to="/profile" style={{ textDecoration: "none" }}>
          プロフィール
        </RouterLink>
        <ColorModeButton />
      </Stack>
    </Flex>
    <Container maxW="container.md" py={8}>
      {children}
    </Container>
  </Box>
)

export default Layout
