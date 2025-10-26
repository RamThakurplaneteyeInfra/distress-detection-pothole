# Local Development Setup

## Prerequisites

- Python 3.11
- Virtual environment (recommended)
- PostgreSQL database access (Render hosted)

## Setup Instructions

### 1. Activate Virtual Environment

```bash
.\venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

The `.env` file has been created with the following configuration:

- **DB_HOST**: Your Render PostgreSQL host
- **DB_PORT**: 5432
- **DB_NAME**: distress_db
- **DB_USER**: distress_db_user
- **DB_PASSWORD**: xZLgwESqa0z9OeMtZiAlYbidFQqLHDMv

### 4. Run the Application

```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## Troubleshooting

### Database Connection Failed

1. Check if your `.env` file exists
2. Verify database credentials are correct
3. Ensure you have internet connectivity to access the Render database

### SAM Model Not Loading

- The SAM model file (`sam_vit_b_01ec64.pth`) should be in the project root
- If missing, the app will attempt to download it automatically

### Port Already in Use

- Change the port in `app.py` if port 5000 is already in use
- Or stop the service using port 5000

## Notes

- The app connects to your hosted PostgreSQL database on Render
- First run may take a minute or two to load the SAM AI model
- All pothole detections are saved to the remote database
