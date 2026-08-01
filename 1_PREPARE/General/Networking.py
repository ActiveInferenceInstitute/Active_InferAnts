import socket
import requests
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import netifaces
import usb.core
import usb.util
import json
from typing import Dict, List, Optional, Union
import logging
from concurrent.futures import ThreadPoolExecutor
import nmap
import scapy.all as scapy
import psutil
from scapy.layers.inet import IP, ICMP

class NetworkUtils:
    """
    A comprehensive collection of modern networking methods, including LAN, Ethernet, USB, Mesh Net, and website interactions.
    This class provides a wide range of utilities for network operations, diagnostics, and information gathering.
    """

    @staticmethod
    def get_local_ip() -> str:
        """
        Retrieves the local IP address of the machine.

        Returns:
            str: The local IP address.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(('10.255.255.255', 1))
                return s.getsockname()[0]
        except Exception as e:
            logging.error(f"Error getting local IP: {e}")
            return '127.0.0.1'

    @staticmethod
    def get_public_ip() -> str:
        """
        Retrieves the public IP address of the machine using an external service.

        Returns:
            str: The public IP address.
        """
        try:
            response = requests.get('https://api.ipify.org', timeout=5)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error(f"Error getting public IP: {e}")
            return "Unable to retrieve public IP"

    @staticmethod
    def list_network_interfaces() -> Dict[str, Dict]:
        """
        Lists all network interfaces and their details.

        Returns:
            Dict[str, Dict]: A dictionary of network interfaces and their details.
        """
        try:
            interfaces = netifaces.interfaces()
            return {interface: netifaces.ifaddresses(interface) for interface in interfaces}
        except Exception as e:
            logging.error(f"Error listing network interfaces: {e}")
            return {}

    @staticmethod
    def start_simple_http_server(port: int = 8000, content: str = 'Hello, world!'):
        """
        Starts a simple HTTP server on the specified port.

        Args:
            port (int): The port to run the server on. Defaults to 8000.
            content (str): The content to serve. Defaults to 'Hello, world!'.
        """
        class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content.encode())

        try:
            with HTTPServer(('localhost', port), SimpleHTTPRequestHandler) as httpd:
                print(f"Serving on port {port}")
                httpd.serve_forever()
        except Exception as e:
            logging.error(f"Error starting HTTP server: {e}")

    @staticmethod
    def list_usb_devices() -> List[str]:
        """
        Lists all connected USB devices.

        Returns:
            List[str]: A list of connected USB device names.
        """
        try:
            devices = usb.core.find(find_all=True)
            return [usb.util.get_string(device, device.iProduct) for device in devices if device.iProduct]
        except Exception as e:
            logging.error(f"Error listing USB devices: {e}")
            return []

    @staticmethod
    def fetch_website_content(url: str, timeout: int = 10, max_bytes: int = 2 * 1024 * 1024) -> Optional[str]:
        """
        Fetches and returns the content of a website.

        Only ``http``/``https`` URLs are accepted (prevents SSRF against internal
        schemes such as ``file://``), and the response body is capped at
        ``max_bytes`` so a large or malicious response cannot exhaust memory.

        Args:
            url (str): The URL of the website to fetch.
            timeout (int): The timeout for the request in seconds. Defaults to 10.
            max_bytes (int): Maximum response body size to accept. Defaults to 2 MiB.

        Returns:
            Optional[str]: The content of the website, or None if an error occurred.
        """
        try:
            parsed = urllib.parse.urlparse(url)
            if parsed.scheme not in ("http", "https"):
                logging.error(f"Refusing to fetch non-http(s) URL scheme: {parsed.scheme or '<none>'}")
                return None
            with requests.get(url, timeout=timeout, stream=True) as response:
                response.raise_for_status()
                chunks = []
                size = 0
                for chunk in response.iter_content(chunk_size=65536):
                    chunks.append(chunk)
                    size += len(chunk)
                    if size > max_bytes:
                        raise ValueError(f"Response exceeds the {max_bytes} byte limit")
                return b"".join(chunks).decode("utf-8", errors="replace")
        except ValueError as e:
            logging.error(f"Error fetching website content: {e}")
            return None
        except requests.RequestException as e:
            logging.error(f"Error fetching website content: {e}")
            return None

    @staticmethod
    def encode_url_parameters(params: Dict[str, str]) -> str:
        """
        Encodes URL parameters.

        Args:
            params (Dict[str, str]): A dictionary of parameters to encode.

        Returns:
            str: The encoded URL parameters.
        """
        return urllib.parse.urlencode(params)

    @staticmethod
    def perform_port_scan(target: str, port_range: range) -> Dict[int, str]:
        """
        Performs a port scan on the specified target.

        Args:
            target (str): The IP address or hostname to scan.
            port_range (range): The range of ports to scan.

        Returns:
            Dict[int, str]: A dictionary of open ports and their services.
        """
        nm = nmap.PortScanner()
        nm.scan(target, arguments=f'-p {port_range.start}-{port_range.stop-1}')
        return {int(port): nm[target]['tcp'][int(port)]['name'] for port in nm[target]['tcp']}

    @staticmethod
    def perform_arp_scan(network: str) -> List[Dict[str, str]]:
        """
        Performs an ARP scan to discover devices on the local network.

        Args:
            network (str): The network to scan, e.g., '192.168.1.0/24'.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing IP and MAC addresses of discovered devices.
        """
        arp_request = scapy.ARP(pdst=network)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        return [{'ip': received.psrc, 'mac': received.hwsrc} for sent, received in answered_list]

    @staticmethod
    def check_connectivity(host: str = '8.8.8.8', port: int = 53, timeout: float = 3) -> bool:
        """
        Checks internet connectivity by attempting to connect to a specified host.

        Args:
            host (str): The host to connect to. Defaults to Google's DNS server.
            port (int): The port to connect to. Defaults to 53 (DNS).
            timeout (float): The timeout for the connection attempt in seconds.

        Returns:
            bool: True if the connection was successful, False otherwise.
        """
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error as ex:
            logging.error(f"Connectivity check failed: {ex}")
            return False

    @staticmethod
    def get_network_usage() -> Dict[str, Dict[str, int]]:
        """
        Retrieves network usage statistics for all network interfaces.

        Returns:
            Dict[str, Dict[str, int]]: A dictionary of network interfaces and their usage statistics.
        """
        try:
            interfaces = netifaces.interfaces()
            usage = {}
            for interface in interfaces:
                stats = psutil.net_io_counters(pernic=True).get(interface)
                if stats:
                    usage[interface] = {
                        'bytes_sent': stats.bytes_sent,
                        'bytes_recv': stats.bytes_recv,
                        'packets_sent': stats.packets_sent,
                        'packets_recv': stats.packets_recv
                    }
            return usage
        except Exception as e:
            logging.error(f"Error getting network usage: {e}")
            return {}

    @staticmethod
    def traceroute(destination: str, max_hops: int = 30) -> List[Dict[str, Union[int, str]]]:
        """
        Performs a traceroute to the specified destination.

        Args:
            destination (str): The IP address or hostname of the destination.
            max_hops (int): The maximum number of hops to trace. Defaults to 30.

        Returns:
            List[Dict[str, Union[int, str]]]: A list of dictionaries containing hop number, IP address, and round-trip time.
        """
        try:
            traceroute_result = []
            for i in range(1, max_hops + 1):
                pkt = IP(dst=destination, ttl=i) / ICMP()
                reply = scapy.sr1(pkt, verbose=0, timeout=5)
                if reply is None:
                    traceroute_result.append({'hop': i, 'ip': '*', 'rtt': '*'})
                elif reply.type == 3:
                    traceroute_result.append({'hop': i, 'ip': reply.src, 'rtt': reply.time})
                    break
                else:
                    traceroute_result.append({'hop': i, 'ip': reply.src, 'rtt': reply.time})
                    if reply.src == destination:
                        break
            return traceroute_result
        except Exception as e:
            logging.error(f"Error performing traceroute: {e}")
            return []
