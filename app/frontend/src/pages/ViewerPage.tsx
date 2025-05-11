import React from 'react';
import { Viewer } from '../components/viewer/Viewer';

interface ViewerPageProps {
  id: string;
}

export const ViewerPage: React.FC<ViewerPageProps> = ({ id }) => {
  return <Viewer id={id} />;
};
