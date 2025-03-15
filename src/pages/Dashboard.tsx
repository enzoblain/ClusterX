import React, { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/core';
import { open } from '@tauri-apps/plugin-dialog';
import Loading from '../components/Loading';
import './Dashboard.css';

const Dashboard: React.FC = () => {
	const [data_folders, setData_folders] = useState<string[]>([]);
	const [loading, setLoading] = useState(true);

	const [showInput, setShowInput] = useState(false);
	const [folderName, setFolderName] = useState('');
	const [newFolderName, setNewFolderName] = useState('');
	const [folderNameError, setFolderNameError] = useState(false);

	useEffect(() => {
		fetchDataFolders();
	}, []);

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

	function editFolderName() {
		setShowInput(false);
		setFolderName('');

		if (newFolderName === folderName) {
			return;
		}

		invoke('rename_dataset', {dataset: folderName, name: newFolderName})
		.then(() => {
			setData_folders((prevDataFolders) =>
			prevDataFolders.map((item) => item === folderName ? newFolderName : item)
			);
		})
		.catch((error) => {
			console.error(error);
		});
	}	

	function disableInput() {
		setShowInput(false);
		setFolderName('');
		setNewFolderName('');
		setFolderNameError(false);
	}

	function displayInput(folder: string) {
		setShowInput(true);
		setFolderName(folder);
	}

	function formatName(name: string) {
		return name.trim();
	}

	function isFolderNameValid(folder: string) {
		folder = formatName(folder);
		const invalidChars = /[<>:"/\\|?*]/;

		if ((folder.length === 0) || 
			((folder != folderName && data_folders.includes(folder))) ||
			(invalidChars.test(folder))
		) {
			setFolderNameError(true);
		} else {
			setFolderNameError(false);
			setNewFolderName(folder);
		}
	}

	const handleFolderNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		const folder = event.target.value;

		isFolderNameValid(folder);
	}

	async function selectFolder() {
		const folder = await open({
			directory: true,
			multiple: false
		});

		if (folder) {
			try {
				await invoke<string>('copy_dataset', { source: folder });
				fetchDataFolders();
			} catch (error) {
				console.error(error);
			}
		}
	}

	return (
		<>
			{loading ? (
				<Loading />
			) : data_folders.length === 0 ? (
				<p>No data folders found</p>
			) : (
				<>
					{showInput && (
						<>
							<div className='rest' onClick={() => disableInput()}></div>
							<div className='rename-box'>
								<input type="text" defaultValue={folderName} onChange={handleFolderNameChange}/>
								<button onClick={() => editFolderName()} 
										className={folderNameError ? 'error' : ''}
										disabled={folderNameError}>Save</button>
							</div>
						</>
					)}
					<div className='dashboard-backtest'>
						{data_folders.map((folder, index) => (
							<div key={index} className='backtests'>
								<div>{folder}</div>
								<button onClick={() => displayInput(folder)}>Edit name</button>
							</div>
						))}
					</div>
					<div className='add-button'>
						<button onClick={selectFolder}>Add a folder</button>
					</div>
				</>
			)}
		</>
	);
};

export default Dashboard;