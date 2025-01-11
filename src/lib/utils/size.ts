function bytesToReadable(bytes: number): string {
  const units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
  const index = Math.floor(Math.log(bytes) / Math.log(1000));
  const value = bytes / Math.pow(1000, index);
  return `${value.toFixed(2)} ${units[index]}`;
}

export default bytesToReadable;