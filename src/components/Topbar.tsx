import './Topbar.css'
import { Link, useLocation } from 'react-router-dom';

const Topbar: React.FC = () => {
    const location = useLocation();

    return (
        <div className="topbar">
            <Link to="/" className="title">ClusterX</Link>
            <div className="links">
                <Link className={location.pathname === "/dashboard" ? "active link" : "link "} to="/dashboard">Dashboard</Link>
            </div>
        </div>
    );
}

export default Topbar;
