"use client"

import React, { useState, ChangeEvent } from 'react';
import axios from 'axios';

type Article = {
    header: string;
    url: string;
};

const Home: React.FC = () => {
    const [keywords, setKeywords] = useState<string>('');
    const [articles, setArticles] = useState<Article[]>([]);
    const [error, setError] = useState<string | null>(null);

    const searchArticles = async () => {
        try {
            const response = await axios.post<{ articles: Article[] }>('http://localhost:5000/articles/find', {
                keywords: keywords.split(',')
            });
            setArticles(response.data.articles);
            setError(null);
        } catch (err) {
            if (axios.isAxiosError(err)) {
                if (err.response?.status === 500) {
                    setError('Internal server error. Please try again later.');
                } else {
                    setError('Failed to fetch articles. Please try again later.');
                }
            } else {
                setError('An unexpected error occurred. Please try again later.');
            }
        }
    };

    const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
        setKeywords(e.target.value);
    };

    return (
        <div className="App">
            <h1>News Article Search</h1>
            <input 
                type="text" 
                value={keywords} 
                onChange={handleInputChange} 
                placeholder="Enter keywords separated by comma" 
            />
            <button onClick={searchArticles}>Search</button>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <ul>
                {articles.map((article, index) => (
                    <li key={index}>
                        <a href={article.url} target="_blank" rel="noopener noreferrer">
                            {article.header}
                        </a>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Home;
