import React, { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/core';
import Loading from '../components/Loading';

const Dashboard: React.FC = () => {
	const [data_folders, setData_folders] = useState<string[]>([]);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		const fetchDataFolders = async () => {

			try{
				const response = await invoke<string[]>('get_data_folders');
				setData_folders(response);
			} catch (error) {
				console.error(error);
			} finally {
				setLoading(false);
			}
		}
		fetchDataFolders();
	}, []);

	return (
		<>
		  	{loading ? (
				<Loading />
			) : (
			(data_folders.length === 0) ? (
				<p>No data folders found</p>
			) : (
				<ul>
					{data_folders.map((folder, index) => (
					<li key={index}>{folder}</li> // Affiche chaque dossier
					))}
				</ul>
			))}
		</>
	);
};

export default Dashboard;