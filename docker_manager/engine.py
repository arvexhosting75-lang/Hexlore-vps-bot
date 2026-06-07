"""Docker Engine wrapper and management"""

import asyncio
import docker
from typing import Optional, Dict, Any, List
from utils.logger import get_logger

logger = get_logger(__name__)


class DockerEngine:
    """Docker engine manager"""

    def __init__(self, socket_path: str = "/var/run/docker.sock"):
        """Initialize Docker engine

        Args:
            socket_path: Path to Docker socket
        """
        self.socket_path = socket_path
        self.client = None

    async def verify_connection(self) -> bool:
        """Verify Docker connection

        Returns:
            True if connected, False otherwise
        """
        try:
            self.client = docker.DockerClient(
                base_url=f"unix://{self.socket_path}", timeout=10
            )
            version = self.client.version()
            logger.info(f"Docker version: {version['Version']}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Docker: {e}")
            return False

    async def create_container(
        self,
        name: str,
        image: str,
        ram_mb: int = 512,
        cpu_shares: int = 1024,
        ports: Optional[Dict[str, int]] = None,
        volumes: Optional[List[str]] = None,
        **kwargs,
    ) -> Optional[str]:
        """Create a Docker container

        Args:
            name: Container name
            image: Docker image
            ram_mb: RAM in MB
            cpu_shares: CPU shares
            ports: Port mappings
            volumes: Volume mappings

        Returns:
            Container ID or None
        """
        if not self.client:
            logger.error("Docker client not initialized")
            return None

        try:
            container = self.client.containers.run(
                image,
                name=name,
                detach=True,
                mem_limit=f"{ram_mb}m",
                cpu_shares=cpu_shares,
                ports=ports or {},
                volumes=volumes or [],
                **kwargs,
            )
            logger.info(f"Container created: {container.id[:12]}")
            return container.id
        except Exception as e:
            logger.error(f"Failed to create container: {e}")
            return None

    async def delete_container(self, container_id: str, force: bool = True) -> bool:
        """Delete a container

        Args:
            container_id: Container ID
            force: Force removal

        Returns:
            True if successful
        """
        if not self.client:
            logger.error("Docker client not initialized")
            return False

        try:
            container = self.client.containers.get(container_id)
            container.remove(force=force)
            logger.info(f"Container deleted: {container_id[:12]}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete container: {e}")
            return False

    async def start_container(self, container_id: str) -> bool:
        """Start a container

        Args:
            container_id: Container ID

        Returns:
            True if successful
        """
        if not self.client:
            logger.error("Docker client not initialized")
            return False

        try:
            container = self.client.containers.get(container_id)
            container.start()
            logger.info(f"Container started: {container_id[:12]}")
            return True
        except Exception as e:
            logger.error(f"Failed to start container: {e}")
            return False

    async def stop_container(self, container_id: str) -> bool:
        """Stop a container

        Args:
            container_id: Container ID

        Returns:
            True if successful
        """
        if not self.client:
            logger.error("Docker client not initialized")
            return False

        try:
            container = self.client.containers.get(container_id)
            container.stop(timeout=10)
            logger.info(f"Container stopped: {container_id[:12]}")
            return True
        except Exception as e:
            logger.error(f"Failed to stop container: {e}")
            return False

    async def restart_container(self, container_id: str) -> bool:
        """Restart a container

        Args:
            container_id: Container ID

        Returns:
            True if successful
        """
        if not self.client:
            logger.error("Docker client not initialized")
            return False

        try:
            container = self.client.containers.get(container_id)
            container.restart(timeout=10)
            logger.info(f"Container restarted: {container_id[:12]}")
            return True
        except Exception as e:
            logger.error(f"Failed to restart container: {e}")
            return False

    async def get_container_stats(self, container_id: str) -> Optional[Dict[str, Any]]:
        """Get container statistics

        Args:
            container_id: Container ID

        Returns:
            Container stats dict or None
        """
        if not self.client:
            logger.error("Docker client not initialized")
            return None

        try:
            container = self.client.containers.get(container_id)
            stats = container.stats(stream=False)
            return stats
        except Exception as e:
            logger.error(f"Failed to get container stats: {e}")
            return None

    async def get_container_logs(self, container_id: str, tail: int = 50) -> Optional[str]:
        """Get container logs

        Args:
            container_id: Container ID
            tail: Number of lines to retrieve

        Returns:
            Logs string or None
        """
        if not self.client:
            logger.error("Docker client not initialized")
            return None

        try:
            container = self.client.containers.get(container_id)
            logs = container.logs(tail=tail).decode()
            return logs
        except Exception as e:
            logger.error(f"Failed to get container logs: {e}")
            return None
