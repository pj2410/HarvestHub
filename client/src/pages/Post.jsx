import { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import PostTitles from '../components/PostTitles';
import CreatePost from '../components/CreatePost';
import url from '../url'

const Post = () => {
    const [posts, setPosts] = useState([]);
    const [refreshing, setRefreshing] = useState(false);
    const [loading, setLoading] = useState(false);
    const [pagination, setPagination] = useState({});
    const [currentPage, setCurrentPage] = useState(1);

    const fetchData = async (page = 1) => {
      setLoading(true);
      try {
        const response = await axios.get(`${url}/Postfetch?page=${page}&limit=10`);
        setPosts(response.data.posts);
        setPagination(response.data.pagination);
        setCurrentPage(page);
      } catch (error) {
        console.error('Error fetching posts:', error);
      } finally {
        setLoading(false);
      }
    };

    const onRefresh = useCallback(() => {
      setRefreshing(true);
      fetchData(1); 
      setTimeout(() => {
        setRefreshing(false);
      }, 2000);
    }, []);

    useEffect(() => {
      fetchData();
    }, []);
  
    return (
      <div className="d-flex flex-column p-4 pb-1" 
      style={{backgroundColor:"#c9d4f8"}}>
      <div className="d-flex flex-column justify-content-between">
          <div style={{width: 'auto' }}>
              <CreatePost onRefresh={onRefresh}/>
          </div>
          <div style={{marginTop:20}}>
            {loading ? (
              <div className="text-center">
                <div className="spinner-border text-primary" role="status">
                  <span className="visually-hidden">Loading...</span>
                </div>
              </div>
            ) : (
              <>
                <PostTitles type="posts" posts={posts} />
                {pagination.totalPages > 1 && (
                  <nav aria-label="Posts pagination" className="mt-4">
                    <ul className="pagination justify-content-center">
                      <li className={`page-item ${!pagination.hasPrev ? 'disabled' : ''}`}>
                        <button 
                          className="page-link" 
                          onClick={() => fetchData(currentPage - 1)}
                          disabled={!pagination.hasPrev}
                        >
                          Previous
                        </button>
                      </li>
                      <li className="page-item active">
                        <span className="page-link">
                          {currentPage} of {pagination.totalPages}
                        </span>
                      </li>
                      <li className={`page-item ${!pagination.hasNext ? 'disabled' : ''}`}>
                        <button 
                          className="page-link" 
                          onClick={() => fetchData(currentPage + 1)}
                          disabled={!pagination.hasNext}
                        >
                          Next
                        </button>
                      </li>
                    </ul>
                  </nav>
                )}
              </>
            )}
          </div>
      </div>
  </div>
    );
  };

export default Post