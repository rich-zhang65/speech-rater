-- Speech Rater Database Schema

-- Users table (basic user info, Auth0 handles authentication)
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Speech recordings table
CREATE TABLE IF NOT EXISTS speech_recordings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    transcription TEXT NOT NULL,
    s3_key VARCHAR(512),
    duration_seconds DECIMAL(10, 2),
    word_count INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Speech grades table
CREATE TABLE IF NOT EXISTS speech_grades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recording_id INT NOT NULL,
    overall_score DECIMAL(5, 2) NOT NULL,
    clarity_score DECIMAL(5, 2) NOT NULL,
    grammar_score DECIMAL(5, 2) NOT NULL,
    vocabulary_score DECIMAL(5, 2) NOT NULL,
    fluency_score DECIMAL(5, 2) NOT NULL,
    detailed_feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recording_id) REFERENCES speech_recordings(id) ON DELETE CASCADE,
    INDEX idx_recording_id (recording_id),
    INDEX idx_overall_score (overall_score)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Improvements suggestions table (normalized for better querying)
CREATE TABLE IF NOT EXISTS improvements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    grade_id INT NOT NULL,
    suggestion TEXT NOT NULL,
    category ENUM('clarity', 'grammar', 'vocabulary', 'fluency', 'general') DEFAULT 'general',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (grade_id) REFERENCES speech_grades(id) ON DELETE CASCADE,
    INDEX idx_grade_id (grade_id),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Strengths table
CREATE TABLE IF NOT EXISTS strengths (
    id INT AUTO_INCREMENT PRIMARY KEY,
    grade_id INT NOT NULL,
    strength TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (grade_id) REFERENCES speech_grades(id) ON DELETE CASCADE,
    INDEX idx_grade_id (grade_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- User progress tracking
CREATE TABLE IF NOT EXISTS user_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    total_recordings INT DEFAULT 0,
    average_score DECIMAL(5, 2),
    last_recording_date TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_progress (user_id),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

