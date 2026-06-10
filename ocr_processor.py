import base64
import requests
import json
from typing import Dict, Any
from PIL import Image
from io import BytesIO
from config_manager import get_api_endpoint, get_back_prompt, get_front_prompt, get_timeout


def encode_image_to_base64(image: Image.Image) -> str:
    """
    Convert a PIL Image to base64 string.
    
    Args:
        image: PIL Image object
        
    Returns:
        Base64 encoded string of the image
    """
    img_buffer = BytesIO()
    image.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode("utf-8")
    return img_base64


def process(image: Image.Image, type_id: int = 0) -> Dict[str, Any]:
    """
    Send image and prompt to OCR API and return the result.
    
    Args:
        image: PIL Image object to process
        prompt: Text prompt for the API (optional, defaults to ID card extraction)
        
    Returns:
        Dictionary containing OCR results from the API response
        
    Raises:
        requests.RequestException: If API call fails
        json.JSONDecodeError: If response is not valid JSON
    """
    try:
        # Encode image to base64
        img_base64 = encode_image_to_base64(image)
        
        headers = {
            "ngrok-skip-browser-warning": "true"
        }

        # Prepare payload
        payload = {
            "img": img_base64,
            "prompt": get_front_prompt() if type_id == 0 else get_back_prompt()
        }
        
        # Call API
        api_endpoint = get_api_endpoint() + '/v1'
        timeout = get_timeout()
        
        response = requests.post(
            api_endpoint,
            headers=headers,
            json=payload,
            timeout=timeout
        )
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Parse and return JSON response
        result = response.json()
        return result
        
    except requests.exceptions.ConnectionError:
        raise Exception("Failed to connect to OCR API. Check your API endpoint URL.")
    except requests.exceptions.Timeout as e:
        timeout = get_timeout()
        raise Exception(f"API request timed out after {timeout} seconds.")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"API returned error: {e.response.status_code} - {e.response.text}")
    except json.JSONDecodeError:
        raise Exception("API response is not valid JSON.")
    except Exception as e:
        raise Exception(f"Error processing image: {str(e)}")


def process_pair(
    front_image: Image.Image,
    back_image: Image.Image
) -> Dict[str, Any]:
    """
    Send both front and back images with respective prompts to the OCR API.

    Args:
        front_image: PIL Image for the front side
        back_image: PIL Image for the back side
        front_prompt: Prompt for the front image
        back_prompt: Prompt for the back image

    Returns:
        Dictionary containing OCR results from the API response
    """
    try:
        front_prompt = get_front_prompt()
        back_prompt = get_back_prompt()

        headers = {
            "ngrok-skip-browser-warning": "true"
        }
        
        payload = {
            "front_img": encode_image_to_base64(front_image),
            "back_img": encode_image_to_base64(back_image),
            "front_prompt": front_prompt,
            "back_prompt": back_prompt
        }

        api_endpoint = get_api_endpoint()
        timeout = get_timeout()

        response = requests.post(
            api_endpoint,
            headers=headers,
            json=payload,
            timeout=timeout
        )
        response.raise_for_status()

        return response.json()

    except requests.exceptions.ConnectionError:
        raise Exception("Failed to connect to OCR API. Check your API endpoint URL.")
    except requests.exceptions.Timeout:
        timeout = get_timeout()
        raise Exception(f"API request timed out after {timeout} seconds.")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"API returned error: {e.response.status_code} - {e.response.text}")
    except json.JSONDecodeError:
        raise Exception("API response is not valid JSON.")
    except Exception as e:
        raise Exception(f"Error processing images: {str(e)}")


def process_with_custom_endpoint(
    image: Image.Image, 
    prompt: str, 
    endpoint: str
) -> Dict[str, Any]:
    """
    Process image with a custom API endpoint.
    
    Args:
        image: PIL Image object to process
        prompt: Text prompt for the API
        endpoint: Custom API endpoint URL
        
    Returns:
        Dictionary containing OCR results
    """
    try:
        img_base64 = encode_image_to_base64(image)
        
        payload = {
            "image_base64": img_base64,
            "prompt": prompt
        }
        
        timeout = get_timeout()
        response = requests.post(endpoint, json=payload, timeout=timeout)
        response.raise_for_status()
        
        return response.json()
        
    except Exception as e:
        raise Exception(f"Error processing with custom endpoint: {str(e)}")

from PIL import ImageOps

def fit_image(img, size=(400, 250)):
    return ImageOps.pad(
        img,
        size,
        color="white",
        centering=(0.5, 0.5)
    )

import re


def parse_front(text: str) -> dict:
    patterns = {
        "so": r"Số\s*:\s*(.+)",
        "ho_va_ten": r"Họ\s*và\s*tên\s*:\s*(.+)",
        "ngay_sinh": r"Ng.*?sinh\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})",
        "gioi_tinh": r"Giới\s*tính\s*:\s*(.+)",
        "quoc_tich": r"Quốc\s*tịch\s*:\s*(.+)",
        "que_quan": r"Quê\s*quán\s*:\s*(.+)",
        "dia_chi_thuong_tru": r"Địa\s*chỉ\s*thường\s*trú\s*:\s*(.+)",
    }

    result = {}

    for field, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        result[field] = match.group(1).strip() if match else None

    return result

def parse_back(text: str) -> dict:
    result = {}

    match = re.search(
        r"Đặc\s*điểm\s*nhận\s*dạng\s*:\s*(.+)",
        text,
        re.IGNORECASE
    )
    result["dac_diem_nhan_dang"] = (
        match.group(1).strip() if match else None
    )

    match = re.search(
        r"(\d{2}/\d{2}/\d{4})",
        text
    )
    result["ngay_cap"] = (
        match.group(1) if match else None
    )

    return result
    
